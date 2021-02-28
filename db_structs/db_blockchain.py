
import pymongo as pmng
import mongoengine as mge
from datetime import datetime
import json
from configparser import ConfigParser
from btc_utils import BTCUtils as Utils
from bson.binary import Binary as BsonBinary


db_config = Utils.load_config('app.conf','mdb');
config_data = dict(
    username =  db_config['username'],
    password =  db_config['passwd'],
    host = db_config['host'],
    port =  int(db_config['port']),
    authentication_source=  db_config['auth_db']
)

def global_connect(conn_alias='chinnus_nas'):
    mge.register_connection(alias=conn_alias, name=db_config['db_blockchain'], **config_data)
    
def global_disconnect(conn_alias='chinnus_nas'):
    mge.disconnect(alias=conn_alias)

class DBBlockchain(mge.Document):
    blkchain_idx = mge.IntField();
    blks_cnt  = mge.IntField();
    blk_first  = mge.IntField();
    blk_last  = mge.IntField();
    is_processed  = mge.BooleanField(default=False);
    
    meta = {
        'db_alias' : 'chinnus_nas',
        'collection' : 'btc_blkchains'
    }
    
    def from_btcpy_obj(self, blkIdx_obj):
        self.blkchain_idx = blkIdx_obj.file;
        #DBBlockchain.blks_cnt = BlocksCnt
        #DBBlockchain.blks_first = btcpy_obj;
        #DBBlockchain.blk_last = BlkLast
        self.save()
    
    
    @staticmethod
    def setup(BlockchainIdx, BlocksCnt, BlkFirst, BlkLast):
        DBBlockchain.blkchain_idx = BlockchainIdx;
        DBBlockchain.blks_cnt = BlocksCnt
        DBBlockchain.blks_first = BlkFirst;
        DBBlockchain.blk_last = BlkLast
    
    def to_json(self):
        return json.dumps({
            blkchain_idx : self.blkchain_idx,
            blks_cnt : self.blks_cnt,
            blk_first : self.blk_first,
            blk_last : self.blk_last,
            is_processed : self.is_processed
        }, indent=2)
    
    

class DBBlock(mge.Document):
    blk_height = mge.IntField()
    blk_hash = mge.StringField()
    blk_hash_prev = mge.StringField()
    blkchain_idx = mge.IntField()
    tx_cnt = mge.IntField();
    is_processed = mge.BooleanField()
    
    meta = {
        'db_alias' : 'chinnus_nas',
        'collection' : 'btc_blks'
    }
    
    @staticmethod
    def setup(BlockHeight, BlockHash, PrevBlockHash, BlockchainIdx, TxCnt=0):
        DBBlock.blk_height = BlockHeight,
        DBBlock.blk_hash = BlockHash,
        DBBlock.blk_hash_prev = PrevBlockHash,
        DBBlock.blkchain_idx = BlockchainIdx,
        DBBlock.tx_cnt = TxCnt
    
    def from_btcpy_obj(self, blkIdx_obj):
        self.blk_height = blkIdx_obj.height;
        self.blk_hash = blkIdx_obj.hash;
        self.blk_hash_prev = blkIdx_obj.prev_hash;
        self.blkchain_idx = blkIdx_obj.file;
        self.tx_cnt = blkIdx_obj.n_tx;
        self.save()

    def to_json(self):
        return json.dumps({
            blk_height : self.blk_height,
            blk_hash : self.blk_hash,
            blk_hash_prev : self.blk_hash_prev,
            blkchain_idx : self.blkchain_idx,
            tx_cnt : self.tx_cnt,
            is_processed : self.is_processed
        }, indent=2)

class DBTxi(mge.EmbeddedDocument):
    txi_idx = mge.IntField()
    txi_is_coinbase = mge.BooleanField()
    prev_txo_txid = mge.StringField()
    prev_txo_idx = mge.IntField()
    btc_addr_from = mge.StringField()
    i_script = mge.StringField()
    i_script_asm = mge.StringField()
    i_script_type = mge.StringField(default='scriptsig')
    is_witness_signed = mge.BooleanField()
    
        
    def from_btcpy_obj(self, idx, txi_obj, is_coinbase=False):        
        if is_coinbase:
            self.txi_idx = 0;
            self.txi_is_coinbase = True;
        else:
            self.txi_idx = idx;
            self.txi_is_coinbase = False;        
            self.prev_txo_txid = txi_obj.txid
            self.prev_txo_idx = txi_obj.txout
            #btc_addr_from = mge.StringField()
            self.i_script = txi_obj.script_sig.hexlify()
            self.i_script_asm = str(txi_obj.script_sig)
            self.i_script_type = txi_obj.script_sig.type
            if txi_obj.witness is not None:
                self.is_witness_signed = True;
            
    
        
    def to_json(self):
        return json.dumps({
            txi_idx : self.txi_idx,
            txi_is_coinbase : self.txi_is_coinbse,
            prev_txo_txid : self.prev_txo_txid,
            prev_txo_idx : self.prev_txo_idx,
            btc_addr_from : self.btc_addr_from,
            i_script : self.i_script,
            i_script_asm : self.i_script_asm,
            i_script_type : self.i_script_type
        }, indent=2)
    
    
class DBTxo(mge.EmbeddedDocument):
    txo_idx = mge.IntField();
    btc_addr_to = mge.StringField();
    btc_value = mge.FloatField();
    o_script = mge.StringField();
    o_script_asm = mge.StringField();
    o_script_type = mge.StringField();
    utxo = mge.BooleanField(default=True);
    utxo_txid = mge.StringField()
    
    
    def from_btcpy_obj(self, txo_obj):
        self.txo_idx = txo_obj.n;        
        self.btc_value = Utils.val_non_satoshi(txo_obj.value);
        self.o_script = txo_obj.script_pubkey.hexlify();
        self.o_script_asm = str(txo_obj.script_pubkey);
        self.o_script_type = txo_obj.script_pubkey.type;
        if txo_obj.script_pubkey.address is not None:
            self.btc_addr_to = str(txo_obj.script_pubkey.address());
        self.utxo = True;
        

    
class DBTx(mge.Document):
    txid = mge.StringField();
    blk_height = mge.IntField();
    #btc_addr_from = mge.StringField();
    txi_cnt = mge.IntField();
    txo_cnt = mge.IntField();
    utxo = mge.BooleanField(default=True);
    txis = mge.EmbeddedDocumentListField(DBTxi);
    txos = mge.EmbeddedDocumentListField(DBTxo);
    
    meta = {
        'db_alias' : 'chinnus_nas',
        'collection' : 'btc_txs'
    }
    
    def set_utxo_spent(self, txo_idx, utxo_status=False, utxo_txid=None):
        self.txos[txo_idx].utxo = utxo_status;
        if utxo_txid is not None:
            self.txos[txo_idx].utxo_txid = utxo_txid;
        
    
    def from_btcpy_obj(self, blkidx_obj, txn_obj):
        self.txid = txn_obj.txid;
        self.blk_height = blkidx_obj.height;
        self.txi_cnt = len(txn_obj.ins);
        self.txo_cnt = len(txn_obj.outs);
        self.utxo = True;
        self.txis = [];
        if txn_obj.is_coinbase():
            for txin in txn_obj.ins:
                txi_obj = DBTxi();
                txi_obj.from_btcpy_obj(txn_obj.ins.index(txin), txin, True)
                self.txis.append(txi_obj)
        else:
            for txin in txn_obj.ins:
                txi_obj = DBTxi();
                txi_obj.from_btcpy_obj(txn_obj.ins.index(txin), txin, False)
                self.txis.append(txi_obj)
                update_fields = { f'set__txos__{txin.txout}__utxo': False,
                                 f'set__txos__{txin.txout}__utxo_txid': self.txid}
                
                DBTx.objects.get(txid=txin.txid).update(**update_fields)
        self.txos = [];
        for txout in txn_obj.outs:
            txo_obj = DBTxo();            
            txo_obj.from_btcpy_obj(txout)
            self.txos.append(txo_obj)
        self.save()
        


class DBUtxo(mge.Document):
    txid = mge.StringField();
    txo_idx = mge.IntField();
    txid_oidx = mge.StringField();
    blkchain_idx = mge.IntField();    
    blk_height = mge.IntField();
    btc_addr_to = mge.StringField();
    btc_value = mge.FloatField();
    o_script = mge.StringField();
    o_script_asm = mge.StringField();
    o_script_type = mge.StringField();
    is_utxo = mge.BooleanField();
    
    
    def delete_spent(self, i_txid, io_idx):
        #DBUtxo.objects.get(txid=i_txid, txo_idx=io_idx).delete()
        txid_oidx_key = i_txid + "-" + str(io_idx);    
            
        try:
            obj_to_delete = DBUtxo.objects(txid_oidx = txid_oidx_key ).first();
            if obj_to_delete is not None:
                obj_to_delete.delete()
        except: #(mge.DoesNotExist) as e:
            #print("Does not exist error{0}: {1}".format(e.args, txid_oidx_key,))
            print("Does not exist error: {0}".format(txid_oidx_key))
        
        
    def del_from_btcpy_obj(self, txn_obj):
        if not txn_obj.is_coinbase():
            for txin in txn_obj.ins:
                self.delete_spent(txin.txid, txin.txout)
    
       
    def add_from_btcpy_obj(self, blkidx_obj, txn_obj, txo_obj):
        try:
            utxo_obj = DBUtxo();
            utxo_obj.txid = txn_obj.txid;
            utxo_obj.txo_idx = txo_obj.n;
            utxo_obj.txid_oidx = txn_obj.txid + "-" + str(txo_obj.n);
            utxo_obj.blkchain_idx = blkidx_obj.file;
            utxo_obj.blk_height = blkidx_obj.height;
            if txo_obj.script_pubkey.address() is not None:
                utxo_obj.btc_addr_to = str(txo_obj.script_pubkey.address());
            utxo_obj.btc_value = Utils.val_non_satoshi(txo_obj.value);
            utxo_obj.o_script = txo_obj.script_pubkey.hexlify();
            utxo_obj.o_script_asm = str(txo_obj.script_pubkey);
            utxo_obj.o_script_type = txo_obj.script_pubkey.type;
            utxo_obj.is_utxo = True;
            utxo_obj.save();
        except (pmng.errors.DuplicateKeyError, mge.errors.NotUniqueError) as e:
            print("Duplicate key error({0}): {1}".format(e.args, utxo_obj.txid_oidx))
        
    def from_btcpy_obj(self, blkidx_obj, txn_obj):      
        for txo_obj in txn_obj.outs:
            self.add_from_btcpy_obj(blkidx_obj, txn_obj, txo_obj);
            
        if not txn_obj.is_coinbase():
            for txi_obj in txn_obj.ins:
                self.delete_spent(txi_obj.txid, txi_obj.txout);

                
    meta = {
        'db_alias' : 'chinnus_nas',
        'collection' : 'btc_utxos'
    }
    
    

class DBDirectory(mge.Document):
    btc_addr = mge.StringField();
    btc_addr_type = mge.StringField();
    btc_addr_is_segwit = mge.BooleanField();
    btc_addr_p2pkh = mge.StringField();
    btc_addr_p2wpkh = mge.StringField();
    btc_addr_p2sh = mge.StringField();
    btc_addr_p2wsh = mge.StringField();
    btc_addr_bech32 = mge.StringField();
    pbk = mge.BinaryField();
    hash160 = mge.BinaryField();
    pvk = mge.BinaryField();
    bal = mge.FloatField();
    bal_asof = mge.DateTimeField();
    utxo = mge.BooleanField(default=True);
    txis = mge.ListField()
    txos = mge.ListField()
    
    meta = {
        'db_alias' : 'chinnus_nas',
        'collection' : 'btc_directory'
    }
