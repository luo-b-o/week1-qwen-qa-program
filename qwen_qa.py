#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通义千问API简单问答程序
作者: 用户
功能: 通过命令行与通义千问API进行问答交互
"""

import os
import requests
import json


def get_api_key():
    """
    获取API密钥
    优先从环境变量获取，如果没有则提示用户输入
    """
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("未找到环境变量 DASHSCOPE_API_KEY")
        api_key = input("请输入您的通义千问API密钥: sk-ca465c9115bf4e659b6d179e2c4e6670").strip()
    return api_key


def select_model():
    """
    让用户选择要使用的模型
    """
    print("\n可选的通义千问模型:")
    print("1. qwen-turbo (快速、经济)")
    print("2. qwen-plus (平衡性能和成本)")
    print("3. qwen-max (高性能，成本较高)")
    print("4. qwen-max-latest (最新版本)")
    
    model_map = {
        "1": "qwen-turbo",
        "2": "qwen-plus", 
        "3": "qwen-max",
        "4": "qwen-max-latest"
    }
    
    while True:
        choice = input("请选择模型 (1-4, 默认为1): ").strip()
        if not choice:
            choice = "1"
        if choice in model_map:
            return model_map[choice]
        else:
            print("无效选择，请输入1-4之间的数字")


def call_qwen_api(api_key, question, model="qwen-turbo"):
    """
    调用通义千问API进行问答
    
    参数:
        api_key (str): 通义千问API密钥
        question (str): 用户提出的问题
        model (str): 使用的模型名称
    
    返回:
        str: API返回的回答内容，如果出错则返回错误信息
    """
    # 通义千问API的URL
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    
    # 请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 请求体
    data = {
        "model": model,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },
        "parameters": {
            "result_format": "message"
        }
    }
    
    try:
        # 发送POST请求
        print(f"正在调用 {model} 模型...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        # 检查响应状态
        if response.status_code == 200:
            result = response.json()
            # 提取回答内容
            answer = result.get("output", {}).get("choices", [{}])[0].get("message", {}).get("content", "")
            return answer
        else:
            error_info = response.text
            try:
                error_json = response.json()
                code = error_json.get("code", "Unknown")
                message = error_json.get("message", "Unknown error")
                error_info = f"错误代码: {code}, 错误信息: {message}"
            except:
                pass
                
            return f"API调用失败，状态码: {response.status_code}, 详细信息: {error_info}"
            
    except requests.exceptions.Timeout:
        return "请求超时，请检查网络连接"
    except requests.exceptions.RequestException as e:
        return f"请求异常: {str(e)}"
    except json.JSONDecodeError:
        return "API返回格式错误"
    except Exception as e:
        return f"未知错误: {str(e)}"


def troubleshoot_403_error():
    """
    提供403错误的排查建议
    """
    print("\n" + "="*60)
    print("🔧 403错误排查指南:")
    print("="*60)
    print("1. 🔑 检查API密钥是否正确:")
    print("   - 登录 https://dashscope.console.aliyun.com/")
    print("   - 在'API Key管理'中确认密钥是否有效")
    print("   - 确保密钥以 'sk-' 开头")
    
    print("\n2. 💰 检查账户状态:")
    print("   - 确认账户已实名认证")
    print("   - 检查账户余额是否充足")
    print("   - 确认已开通通义千问服务")
    
    print("\n3. 🎯 检查模型权限:")
    print("   - 某些模型可能需要单独申请权限")
    print("   - 建议先尝试 qwen-turbo 模型（通常默认可用）")
    
    print("\n4. 🌍 检查网络环境:")
    print("   - 确保网络可以正常访问阿里云服务")
    print("   - 如果在公司网络，可能需要联系IT部门")
    
    print("\n5. 📞 联系技术支持:")
    print("   - 如果以上都确认无误，联系阿里云技术支持")
    print("="*60)


def main():
    """
    主函数：实现问答交互循环
    """
    print("=" * 50)
    print("欢迎使用通义千问问答程序！")
    print("输入 'quit' 或 'exit' 退出程序")
    print("=" * 50)
    
    # 获取API密钥
    api_key = get_api_key()
    if not api_key:
        print("API密钥不能为空！")
        return
    
    # 选择模型
    model = select_model()
    
    # 问答循环
    while True:
        try:
            # 获取用户输入
            question = input("\n请输入您的问题: ").strip()
            
            # 检查退出条件
            if question.lower() in ['quit', 'exit', '退出']:
                print("感谢使用，再见！")
                break
            
            # 检查空输入
            if not question:
                print("问题不能为空，请重新输入")
                continue
            
            # 调用API获取回答
            print("\n正在思考中...")
            answer = call_qwen_api(api_key, question, model)
            
            # 显示回答
            print(f"\n通义千问回答:\n{answer}")
            
            # 如果出现403错误，提供排查建议
            if "403" in answer or "AccessDenied" in answer:
                troubleshoot_403_error()
                retry = input("\n是否要重试？(y/n): ").strip().lower()
                if retry != 'y':
                    break
                else:
                    # 重新选择模型
                    model = select_model()
            
        except KeyboardInterrupt:
            print("\n\n程序被用户中断，再见！")
            break
        except Exception as e:
            print(f"\n程序出现错误: {str(e)}")


if __name__ == "__main__":
    main()