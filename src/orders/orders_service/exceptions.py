# 注文が存在しないことを通知する例外
class OrderNotFoundError(Exception):
    pass

# API統合エラーが発生していることを通知する例外
class APIIntegrationError(Exception):
    pass

# 実行しようとしているアクションが無効であることを通知する例外
class InvalidActionError(Exception):
    pass
