from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class UnitOfWork:

    def __init__(self):
        # セッションファクトリオブジェクトを取得
        self.session_maker = sessionmaker(
            bind=create_engine("sqlite:///src/orders/orders.db")
        )

    def __enter__(self):
        # 新しいデータベースセッションを開く
        self.session = self.session_maker()
        # UnitOfWorkオブジェクトのインスタンスを返す
        return self

    # コンテキストの実行中に発生した例外にアクセスできるようにする
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 例外が発生したかどうかチェック
        if exc_type is not None:
            # 例外が発生した場合、セッションをロールバックして閉じる
            self.session.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()   # SQLAlchemyのcommitメソッドのWrapper

    def rollback(self):
        self.session.rollback()  # SQLAlchemyのrollbackメソッドのWrapper
