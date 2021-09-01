_base_ = [
    '../_base_/models/fcn_r50-d8.py', '../_base_/datasets/ai2thor.py',
    '../_base_/default_runtime.py', '../_base_/schedules/schedule_80k.py'
]
model = dict(
    decode_head=dict(num_classes=120), auxiliary_head=dict(num_classes=120),
    pretrained='open-mmlab://resnet50_v1c', backbone=dict(depth=50))
