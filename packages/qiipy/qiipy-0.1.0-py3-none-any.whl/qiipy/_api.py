from apywrapper import Apy, get, post, delete, patch
from ._models import Comment


class Qiipy(Apy):
    def __init__(self, access_token: str, host: str = "https://qiita.com/api/v2"):
        super().__init__(host=host, headers={"Authorization": f"Bearer {access_token}"})

    @get("/comments/{comment_id}")
    def get_comment(self, comment_id: str):
        """コメントを取得する

        Args:
            comment_id: コメントid
        Returns:
            Comment
        """
        return Comment, {"comment_id": comment_id}

    @delete("/comments/{comment_id}")
    def delete_comment(self, comment_id: str):
        """コメントを削除する

        Args:
            comment_id: コメントid
        Returns:
            None
        """
        return None, {"comment_id": comment_id}

    @patch("/comments/{comment_id}")
    def update_comment(self, comment_id: str, comment_text: str):
        """コメントを更新する

        Args:
            comment_id: コメントid
            comment_text: コメントの本文
        Returns:
            Comment
        """
        return Comment, {"comment_id": comment_id, "body": comment_text}

    @get("/items/{item_id}/comments")
    def get_all_comments(self, article_id: str):
        """記事についているコメントをすべて取得する

        Args:
            article_id: 記事id(item_id)
        Returns:
            List[Comment]
        """
        return Comment, {"item_id": article_id}

    @post("/items/{item_id}/comments")
    def send_comment(self, article_id: str, comment_text: str):
        """記事にコメントを投稿する

        Args:
            article_id: 記事id(item_id)
        Returns:
            Comment
        """
        return Comment, {"item_id": article_id, "body": comment_text}
