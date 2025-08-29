#!/usr/bin/env python3
"""
ヘルプデスクエージェント全体を実行するスクリプト
"""

import sys
import os
from pathlib import Path

# スクリプトの親ディレクトリ（chapter4）をPythonパスに追加
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.insert(0, str(project_root))

from src.agent import HelpDeskAgent
from src.configs import Settings
from src.tools.search_xyz_manual import search_xyz_manual
from src.tools.search_xyz_qa import (
    search_xyz_qa,
)
import weave

@weave.op()
def main(question: str):
    # 設定を読み込み
    print("設定を読み込み中...")
    settings = Settings()

    # ヘルプデスクエージェントを初期化
    print("ヘルプデスクエージェントを初期化中...")
    agent = HelpDeskAgent(
        settings=settings,
        tools=[search_xyz_manual, search_xyz_qa],
    )
    
    print("質問:", question)
    print("\n" + "="*50)
    print("ヘルプデスクエージェントを実行中...")
    print("="*50)
    
    # エージェントを実行
    try:
        result = agent.run_agent(question)
        
        print("\n" + "="*50)
        print("回答:")
        print("="*50)
        print(result.answer)
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    return result.answer

if __name__ == "__main__":
    settings = Settings()
    weave.init(settings.weave_project)
    # 質問を設定
    question = """
お世話になっております。

現在、XYZシステムを利用しており、以下の点についてご教示いただければと存じます。

1. 特定のプロジェクトに対してのみ通知を制限する方法について
特定のプロジェクトに対してのみ通知を制限する方法についてお教えいただけますと幸いです。

2. パスワードに利用可能な文字の制限について
当該システムにてパスワードを設定する際、使用可能な文字の範囲（例：英数字、記号、文字数制限など）について詳しい情報をいただけますでしょうか。安全かつシステムでの認証エラーを防ぐため、具体的な仕様を確認したいと考えております。

お忙しいところ恐縮ですが、ご対応のほどよろしくお願い申し上げます。
"""
    main(question)
