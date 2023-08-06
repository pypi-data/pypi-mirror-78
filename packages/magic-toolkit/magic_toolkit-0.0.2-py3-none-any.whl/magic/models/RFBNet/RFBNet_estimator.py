from magic.torch import TorchEstimator
from magic.data import ImgDataset
from torch import optim
from .data import BaseTransform
from .RFBNet import RFBNet, multibox
from .layers.functions import Detect, PriorBox
from .utils.nms_wrapper import nms
from .layers.modules import MultiBoxLoss
from .utils.visualize import *
from .transform import Transfrom


class RFBNet_Estimator(TorchEstimator):
    def __init__(self, config):
        super(RFBNet_Estimator, self).__init__(config)
        self.cfg = config
        self.init_model()

    def init_model(self):
        self.cuda = True
        priorbox = PriorBox(self.cfg.PriorBox_Config)
        with torch.no_grad():
            self.priors = priorbox.forward()
            if self.cuda:
                self.priors = self.priors.cuda()

        self.criterion = MultiBoxLoss(self.cfg.num_classes,
                                      self.cfg.overlap_thresh,
                                      self.cfg.prior_for_matching,
                                      self.cfg.bkg_label,
                                      self.cfg.neg_mining,
                                      self.cfg.neg_pos,
                                      self.cfg.neg_overlap,
                                      self.cfg.encode_target)

        self.net = RFBNet('train', self.cfg.img_dim, multibox(self.cfg.num_classes), self.cfg.num_classes)

        # # load trained model
        # state_dict = torch.load(self.cfg.pre_trained)
        # from collections import OrderedDict
        # new_state_dict = OrderedDict()
        # for k, v in state_dict.items():
        #     head = k[:7]
        #     if head == 'module.':
        #         name = k[7:]  # remove `module.`
        #     else:
        #         name = k
        #     new_state_dict[name] = v
        # self.net.load_state_dict(new_state_dict)
        # self.net.eval()
        # print('Finished loading model!')
        if self.cuda:
            self.net = self.net.cuda()
        else:
            self.net = self.net.cpu()

        self.model = nn.DataParallel(self.net)
        self.model.eval()

        self.transform = BaseTransform(self.cfg.img_dim, self.cfg.rgb_means, (2, 0, 1))
        self.detection = Detect(self.cfg.num_classes, 0, self.cfg.PriorBox_Config)

    def fit(self):
        transform = Transfrom(self.cfg.img_dim, self.cfg.rgb_means, self.cfg.p)
        dataset = ImgDataset(self.cfg.train_data_path, transform)

        optimizer = optim.SGD(self.model.parameters(), lr = self.cfg.lr_init,
                              momentum=self.cfg.momentum, weight_decay=self.cfg.weight_decay)

        self.backward_optim(dataset, self.loss_fn, optimizer)


    def loss_fn(self, net, batch_data):
        images = Variable(torch.stack(batch_data["img"], 0).cuda())
        out = net(images)
        targets = [Variable(anno.cuda()) for anno in batch_data['target']]
        loss_l, loss_c = self.criterion(out, self.priors, targets)
        loss = loss_l + loss_c
        return loss


    def predict(self, input):
        self.phase = "test"
        img = input
        scale = torch.Tensor([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])
        if self.cuda:
            scale = scale.cuda()

        img = self.pre_process(img)  # 前处理
        outputs = self.model(img)  # 前向
        preds = self.post_process(outputs, self.priors, scale)  # 后处理
        pt = []
        for class_id, class_collection in enumerate(preds):
            if len(class_collection) > 0:
                for i in range(class_collection.shape[0]):
                    pt.append(class_collection[i])
        return pt


    def pre_process(self, img):
        return self.transform(img).unsqueeze(0)


    def post_process(self, outputs, priors, scale):
        boxes, scores = self.detection.forward(outputs, priors)
        boxes = boxes[0]
        scores = scores[0]

        # scale each detection back up to the image
        boxes *= scale
        boxes = boxes.cpu().numpy()
        scores = scores.cpu().numpy()

        all_boxes = [[] for _ in range(self.cfg.num_classes)]

        for j in range(1, self.cfg.num_classes):
            inds = np.where(scores[:, j] > self.cfg.confidence_thresh)[0]
            if len(inds) == 0:
                all_boxes[j] = np.zeros([0, 5], dtype=np.float32)
                continue
            c_bboxes = boxes[inds]
            c_scores = scores[inds, j]
            c_dets = np.hstack((c_bboxes, c_scores[:, np.newaxis])).astype(
                np.float32, copy=False)
            keep = nms(c_dets, self.cfg.iou_thresh)
            c_dets = c_dets[keep, :]
            all_boxes[j] = c_dets

        return all_boxes
