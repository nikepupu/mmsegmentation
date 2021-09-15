_base_ = [
    '../_base_/models/deeplabv3plus_r50-d8.py', '../_base_/datasets/ai2thor.py',
    '../_base_/default_runtime.py', '../_base_/schedules/schedule_240k.py'
]
model = dict(
    decode_head=dict(num_classes=120), auxiliary_head=dict(num_classes=120))
