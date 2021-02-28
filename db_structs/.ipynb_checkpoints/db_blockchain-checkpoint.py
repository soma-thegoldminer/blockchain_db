
class DbBlockchain:
    db_cln = 'btc_blkchains';
    blkchain_idx = 0;
    blks_cnt  = 0;
    blk_first  = 0;
    blk_last  = 0;
    is_processed  = False;
    
    def __init__(self):
        pass;
    
    @staticmethod
    def setup(BlockchainIdx, BlocksCnt, BlkFirst, BlkLast):
        self.blkchain_idx = BlockchainIdx;
        self.blks_cnt = BlocksCnt
        self.blks_first = BlkFirst;
        self.blk_last = BlkLast
    
    def to_json(self):
        return json.dumps({
            blkchain_idx : self.blkchain_idx,
            blks_cnt : self.blks_cnt,
            blk_first : self.blk_first,
            blk_last : self.blk_last,
            is_processed : self.is_processed
        }, indent=2)

class DbBlock:
    db_cln = 'btc_blks';
    blk_height = 0
    blk_hash = 0
    blk_hash_prev = 0
    blkchain_idx = 0
    tx_cnt = 0;
    is_processed = False;
    
    @staticmethod
    def setup(BlockHeight, BlockHash, PrevBlockHash, BlockchainIdx, TxCnt=0):
        blk_height = BlockHeight,
        blk_hash = BlockHash,
        blk_hash_prev = PrevBlockHash,
        blkchain_idx = BlockchainIdx,
        tx_cnt = TxCnt
        

    def to_json(self):
        return json.dumps({
            blk_height : self.blk_height,
            blk_hash : self.blk_hash,
            blk_hash_prev : self.blk_hash_prev,
            blkchain_idx : self.blkchain_idx,
            tx_cnt : self.tx_cnt,
            is_processed : self.is_processed
        }, indent=2)
    
class DbTxi:
    db_cln = 'btc_txs';
    txi_idx = 0;
    txi_is_coinbase = False;
    prev_txo_txid = 0;
    prev_txo_idx = 0;
    btc_addr_from = 0;
    i_script = 0;
    i_script_asm = 0;
    i_script_type = 'scriptsig'
    
        
    def to_json(self):
        return json.dumps({
            txi_idx : self.txi_idx,
            txi_is_coinbase : self.txi_is_coinbse,
            prev_txo_txid : self.prev_txo_txid,
            prev_txo_idx : self.prev_txo_idx,
            btc_addr_from : 0,
            i_script : 0,
            i_script_asm : 0,
            i_script_type : 'scriptsig'
        }, indent=2)
    
    
class DbTxo:
    db_cln = 'btc_txs';
    txo_idx = 0;
    btc_addr_to = 0;
    btc_amt = 0.000;
    o_script = 0;
    o_script_asm = 0;
    o_script_type = 0;
    utxo = True;
    txo_txid = 0
    
class DbTx:
    db_cln = 'btc_txs';
    txid = 0;
    blk_height = 0;
    btc_addr_from = 0;
    txi_cnt = 0;
    txo_count = 0;
    utxo = True;
    txis = [];
    txos = [];
    
class DbDirectory:
    db_cln = 'btc_directory';
    btc_addr = 0;
    btc_addr_type = 0;
    btc_addr_is_segwit = 0;
    btc_addr_p2pkh = 0;
    btc_addr_p2wpkh = 0;
    btc_addr_p2sh = 0;
    btc_addr_p2wsh = 0;
    btc_addr_bech32 = 0;
    pbk = 0;
    hash160 = 0;
    pvk = 0;
    bal = 0;
    bal_asof = 0;
    utxo = True;
    txis = []
    txos = []
