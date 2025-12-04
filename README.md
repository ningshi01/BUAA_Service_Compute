# BUAA_Service_Compute
BUAA-服务计算相关-极简化微服务应用

Service-Compute
本项目共包含四个微服务，但只是为了本课程实现的简化版作业，无较长的调用链路。
本项目是一个基于微服务架构的演示应用，旨在展示如何使用 Docker 和 Kubernetes 构建、部署和管理分布式服务。项目包含前端界面和三个独立的后端服务，分别负责计算逻辑、随机数生成和缓存管理。

项目结构

```text
service-compute/
├── compute-backend/        # 计算服务
│   ├── app.py             # Flask 应用逻辑
│   ├── Dockerfile         
│   ├── deployment.yaml    # K8s 部署配置
│   └── requirements.txt   
├── random-backend/         # 随机数服务
│   ├── app.py
│   ├── Dockerfile
│   ├── deployment.yaml
│   └── requirements.txt
├── redis/                  # 缓存服务 (包含 Redis 数据库和 API 包装器)
│   ├── app.py
│   ├── Dockerfile
│   ├── deployment.yaml
│   └── requirements.txt
└── frontend/               # 前端服务
    ├── index.html         # 用户界面
    ├── nginx.conf         # Nginx 配置
    ├── Dockerfile
    └── deployment.yaml
```