#!/usr/bin/env python

import json
import hashlib

#block = {}
#
#block["id"] = 1
#block["contract"] = "I will pay so and so money"
#block["amount"] = 45.00
#block["from"] = "email@email.com"
#block["to"] = "email@email2.com"
#block["previous_hash"] = "0"
#
#print json.dumps(block)
#
#def format_block(block):
#    # format block in the same way so the hash is always the same
#    # json.dumps will not always output keys in the same order
#    out = ""
#
#    out += str(block["id"]) + "\n"
#    out += block["contract"] + "\n"
#    out += str(block["amount"]) + "\n"
#    out += block["from"] + "\n"
#    out += block["to"]
#
#    return out
#
#def hash_block(block):
#    m = hashlib.sha256()
#    m.update(format_block(block))
#    m.update(block["previous_hash"])
#    return m.hexdigest()
#
#print format_block(block)
#print hash_block(block)
#
#block2 = {}
#
#block2["id"] = 2
#block2["contract"] = "I paided so and so"
#block2["amount"] = 45.00
#block2["from"] = "email2@email.com"
#block2["to"] = "email@email.com"
#block2["previous_hash"] = hash_block(block)
#
#print format_block(block2)
#print hash_block(block2)

from peewee import *

db = SqliteDatabase('chain.db')

class Block(Model):
    contract = TextField()
    amount = FloatField()
    from_email = TextField()
    to_email = TextField()
    prev_hash = TextField()

    class Meta:
        database = db

    def as_dict(self):
        d = {}

        # include each field here
        d["contract"] = self.contract
        d["amount"] = self.amount
        d["from_email"] = self.from_email
        d["to_email"] = self.to_email
        d["prev_hash"] = self.prev_hash

        d["this_hash"] = self.hash_block()

        return d

    def hash_block(self):
        m = hashlib.sha256()

        # include each field here
        m.update(self.contract)
        m.update(str(self.amount))
        m.update(self.from_email)
        m.update(self.to_email)
        m.update(self.prev_hash)

        return m.hexdigest()


from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/blockchain', methods=['GET'])
def list_blockchain():
    block_chain = []

    for block in Block.select():
        block_chain.append(block.as_dict())

    return json.dumps(block_chain)

@app.route('/block', methods=['POST'])
def create_block():
    # if the user did not supply anything, error
    if not request.json:
        abort(400)

    contract = TextField()
    amount = FloatField()
    from_email = TextField()
    to_email = TextField()
    prev_hash = TextField()

    last_block = Block.select().order_by(Block.id.desc()).get()

    new_block = Block(
            contract=request.json["contract"],
            amount=request.json["amount"],
            from_email=request.json["from_email"],
            to_email=request.json["to_email"],
            prev_hash=last_block.hash_block()
            )
    new_block.save()

    return "200 OK"


if __name__ == '__main__':
    db.connect()

    if not Block.table_exists():
        db.create_tables([Block])

        genesis_block = Block(
                contract="asdf",
                amount=123.0,
                from_email="test post",
                to_email="please ignore",
                prev_hash="0"
                )
        genesis_block.save()

    app.run(debug=True) # do not run in prod!

