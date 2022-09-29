---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''

---

name: 🐛 Bug Report
# title: " "
description: Problems with YOLOv6
labels: [bug, triage]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for submitting a YOLOv6 🐛 Bug Report!

  - type: checkboxes
    attributes:
      label: Search before asking
      description: >
        Please search the [issues](https://github.com/meituan/YOLOv6/issues) to see if a similar bug report already exists.
      options:
        - label: >
            I have searched the YOLOv6 [issues](https://github.com/meituan/YOLOv6/issues) and found no similar bug report.
          required: true

  - type: dropdown
    attributes:
      label: YOLOv6 Component
      description: |
        Please select the part of YOLOv6 where you found the bug.(请选择bug所在的模块)
      multiple: true
      options:
        - "Training"（训练）
        - "Evaluation" （评估）
        - "Inference" （推理及结果可视化）
        - "Export"（模型导出）
        - "Quantization(including QAT, PTQ ...)"（量化部分，包括QAT训练，PTQ等）
        - "Multi-GPU"（多卡训练）
        - "TensorRT"（TRT部署）
        - "Other"（其他）
    validations:
      required: false

  - type: textarea
    attributes:
      label: Bug
      description: Provide console output with error messages and/or screenshots of the bug.
      placeholder: |
        💡 ProTip! Include as much information as possible (screenshots, logs, tracebacks etc.) to receive the most helpful response.（请提供bug相关的报错日志或截图等详细信息）
    validations:
      required: true

  - type: textarea
    attributes:
      label: Environment
      description: Please specify the software and hardware you used to produce the bug.（运行环境信息）
      placeholder: |
        - YOLO: YOLOv6 v2.0 torch 1.8.0+cu111 CUDA:0 (A100-SXM4-40GB, 40536MiB)
        - OS: Ubuntu 20.04
        - Python: 3.8
    validations:
      required: false

  - type: textarea
    attributes:
      label: Minimal Reproducible Example
      description: >
        When asking a question, people will be better able to provide help if you provide code that they can easily understand and use to **reproduce** the problem.（请提供能复现这个bug的相关命令及配置超参等信息）
      placeholder: |
        ```
        # Code to reproduce your issue here
        ```
    validations:
      required: false

  - type: textarea
    attributes:
      label: Additional
      description: Anything else you would like to share?

  - type: checkboxes
    attributes:
      label: Are you willing to submit a PR?
      description: >
        (Optional) We encourage you to submit a [Pull Request](https://github.com/meituan/YOLOv6/pulls) (PR) to help improve YOLOv6 for everyone, especially if you have a good understanding of how to implement a fix or feature.
      options:
        - label: Yes I'd like to help by submitting a PR!