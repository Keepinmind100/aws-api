from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
from typing import List, Optional
import os


app = FastAPI(title="AWS IAM Manager API")

# AWS 클라이언트 설정
iam_client = boto3.client('iam')

# Pydantic 모델
class UserCreate(BaseModel):
    username: str
    group_names: Optional[List[str]] = None
    policy_arns: Optional[List[str]] = None

class UserResponse(BaseModel):
    username: str
    arn: str
    created_date: str

@app.post("/users/", response_model=UserResponse)
async def create_iam_user(user: UserCreate):
    try:
        # IAM 사용자 생성
        response = iam_client.create_user(UserName=user.username)
        
        # 그룹에 사용자 추가
        if user.group_names:
            for group_name in user.group_names:
                iam_client.add_user_to_group(
                    GroupName=group_name,
                    UserName=user.username
                )
        
        # 정책 연결
        if user.policy_arns:
            for policy_arn in user.policy_arns:
                iam_client.attach_user_policy(
                    UserName=user.username,
                    PolicyArn=policy_arn
                )
        
        return UserResponse(
            username=response['User']['UserName'],
            arn=response['User']['Arn'],
            created_date=str(response['User']['CreateDate'])
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/", response_model=List[UserResponse])
async def list_iam_users():
    try:
        response = iam_client.list_users()
        return [
            UserResponse(
                username=user['UserName'],
                arn=user['Arn'],
                created_date=str(user['CreateDate'])
            )
            for user in response['Users']
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/users/{username}")
async def delete_iam_user(username: str):
    try:
        # 연결된 정책 분리
        attached_policies = iam_client.list_attached_user_policies(UserName=username)
        for policy in attached_policies['AttachedPolicies']:
            iam_client.detach_user_policy(
                UserName=username,
                PolicyArn=policy['PolicyArn']
            )
        
        # 그룹에서 사용자 제거
        groups = iam_client.list_groups_for_user(UserName=username)
        for group in groups['Groups']:
            iam_client.remove_user_from_group(
                GroupName=group['GroupName'],
                UserName=username
            )
        
        # 사용자 삭제
        iam_client.delete_user(UserName=username)
        return {"message": f"User {username} successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 