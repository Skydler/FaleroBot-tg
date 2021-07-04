from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
import db
import hashlib


class WebSite(db.Base):
    __tablename__ = "website"

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    website_hash = Column(String, nullable=False)

    def __init__(self, url, content):
        self.url = url
        self.website_hash = self._hash_content(content)

    def is_same_content(self, new_content):
        new_hash = self._hash_content(new_content)
        return new_hash == self.website_hash

    def update_content(self, new_content):
        self.website_hash = self._hash_content(new_content)

    def _hash_content(self, content):
        return hashlib.md5(content.encode()).hexdigest()
