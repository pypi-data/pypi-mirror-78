from .topic_map_util import (
    expand_worker,
    expand_group_worker,
    expand_list,
    topic_id_to_multicast_addr,
    check_topic_id_to_string_map)

topic_id_to_string_map = check_topic_id_to_string_map(expand_list([
  # 237.15.0.1        0x0000ED0F0001xxxx: bitmex
                     (0x0000ED0F00011000, 'bitmex_ws_topic_event'),
  expand_group_worker(0x0000ED0F00011100, 'bitmex_ws_orderBookL2_',  num_group=6, num_worker=4),
  expand_group_worker(0x0000ED0F00011200, 'bitmex_ws_orderBook10_',  num_group=6, num_worker=4),
  expand_group_worker(0x0000ED0F00011300, 'bitmex_ws_trade_',        num_group=6, num_worker=4),
        expand_worker(0x0000ED0F00011400, 'bitmex_ws_instrument_',   num_worker=4),
        expand_worker(0x0000ED0F00011500, 'bitmex_ws_liquidation_',  num_worker=4),
        expand_worker(0x0000ED0F00019000, 'bitmex_ws_private_',      num_worker=4),

  # 237.15.0.2       0x0000ED0F0002xxxx: bitfinex
                     (0x0000ED0F00021000, 'bitfinex_v2_ws_topic_event'),
  expand_group_worker(0x0000ED0F00021100, 'bitfinex_v2_ws_book_',    num_group=6, num_worker=4),
  expand_group_worker(0x0000ED0F00021200, 'bitfinex_v2_ws_rawBook_', num_group=6, num_worker=4),
  expand_group_worker(0x0000ED0F00021300, 'bitfinex_v2_ws_trades_',  num_group=6, num_worker=4),
  expand_group_worker(0x0000ED0F00021400, 'bitfinex_v2_ws_etc_',     num_group=6, num_worker=4),
        expand_worker(0x0000ED0F00041500, 'bitfinex_v2_ws_private_', num_worker=4),

  # 237.15.0.3        0x0000ED0F0003xxxx: gdax
                     (0x0000ED0F00031000, 'gdax_ws_topic_event'),
  expand_group_worker(0x0000ED0F00031100, 'gdax_ws_level2_',         num_group=6, num_worker=4),
  expand_group_worker(0x0000ED0F00031200, 'gdax_ws_full_',           num_group=6, num_worker=4),

  # 237.15.0.4        0x0000ED0F0004xxxx: binance
                     (0x0000ED0F00041000, 'binance_ws_topic_event'),
  expand_group_worker(0x0000ED0F00041100, 'binance_ws_depth_',       num_group=9, num_worker=4),
  expand_group_worker(0x0000ED0F00041200, 'binance_ws_depth20_',     num_group=9, num_worker=4),
  expand_group_worker(0x0000ED0F00041300, 'binance_ws_trade_',       num_group=9, num_worker=4),
        expand_worker(0x0000ED0F00041400, 'binance_ws_private_',     num_worker=4),
        expand_worker(0x0000ED0F00042000, 'binance_rest_depth_',     num_worker=4),
        expand_worker(0x0000ED0F00042100, 'binance_rest_private_',   num_worker=4),

  # 237.15.0.5        0x0000ED0F0005xxxx: bittrex
                     (0x0000ED0F00051000, 'bittrex_ws_topic_event'),
        expand_worker(0x0000ED0F00051100, 'bittrex_rest_private_',   num_worker=4),

  # 237.15.0.6        0x0000ED0F0006xxxx: gemini

  # 237.15.0.7        0x0000ED0F0007xxxx: coinone
                     (0x0000ED0F00071000, 'coinone_ws_topic_event'),
  expand_group_worker(0x0000ED0F00071100, 'coinone_ws_depth_',       num_group=16, num_worker=2),
  expand_group_worker(0x0000ED0F00071200, 'coinone_ws_trade_',       num_group=16, num_worker=2),
  expand_group_worker(0x0000ED0F00071300, 'coinone_ws_ticker_',      num_group=16, num_worker=2),

  # 237.15.0.8        0x0000ED0F0008xxxx: bithumb
                     (0x0000ED0F00081000, 'bithumb_ws_topic_event'),
  expand_group_worker(0x0000ED0F00081100, 'bithumb_ws_depth_',       num_group=16, num_worker=2),
  expand_group_worker(0x0000ED0F00081200, 'bithumb_ws_trade_',       num_group=16, num_worker=2),
  expand_group_worker(0x0000ED0F00081400, 'bithumb_ws_quote_',       num_group=16, num_worker=2),
  expand_group_worker(0x0000ED0F00081300, 'bithumb_ws_ticker_',      num_group=16, num_worker=2),

  # 237.15.0.9        0x0000ED0F0009xxxx: poloniex

  # 237.15.0.10       0x0000ED0F000Axxxx: huobi
                     (0x0000ED0F000A1000, 'huobi_ws_topic_event'),
  expand_group_worker(0x0000ED0F000A1100, 'huobi_ws_depth_',         num_group=9, num_worker=4),
  expand_group_worker(0x0000ED0F000A1200, 'huobi_ws_trade_',         num_group=9, num_worker=4),
        expand_worker(0x0000ED0F000A2100, 'huobi_rest_private_',     num_worker=4),

  # 237.15.0.11       0x0000ED0F000Bxxxx: okex
                     (0x0000ED0F000B1000, 'okex_ws_topic_event'),
  expand_group_worker(0x0000ED0F000B1100, 'okex_ws_spot_depth_fullbook_',      num_group=16, num_worker=4),
  expand_group_worker(0x0000ED0F000B1200, 'okex_ws_spot_depth_diff_',          num_group=16, num_worker=4),
  expand_group_worker(0x0000ED0F000B1300, 'okex_ws_spot_depth_20_',            num_group=16, num_worker=4),
  expand_group_worker(0x0000ED0F000B1400, 'okex_ws_spot_deals_',               num_group=16, num_worker=4),
  expand_group_worker(0x0000ED0F000B2000, 'okex_ws_futureusd_depth_fullbook_', num_group=8, num_worker=4),
  expand_group_worker(0x0000ED0F000B2100, 'okex_ws_futureusd_depth_diff_',     num_group=8, num_worker=4),
  expand_group_worker(0x0000ED0F000B2200, 'okex_ws_futureusd_depth_20_',       num_group=8, num_worker=4),
  expand_group_worker(0x0000ED0F000B2300, 'okex_ws_futureusd_trade_',          num_group=8, num_worker=4),
  expand_group_worker(0x0000ED0F000B2400, 'okex_ws_futureusd_index_',          num_group=8, num_worker=4),

  # 237.15.0.12       0x0000ED0F000Cxxxx: upbit
                     (0x0000ED0F000C1000, 'upbit_ws_topic_event'),
  expand_group_worker(0x0000ED0F000C1100, 'upbit_ws_depth_',                   num_group=1, num_worker=4),
  expand_group_worker(0x0000ED0F000C1200, 'upbit_ws_trade_',                   num_group=1, num_worker=4),

  # 237.15.0.13       0x0000ED0F000Dxxxx: bitflyer
                     (0x0000ED0F000D1000, 'bitflyer_pubnub_topic_event'),
  expand_group_worker(0x0000ED0F000D1100, 'bitflyer_pubnub_board_snapshot_',   num_group=2, num_worker=4),
  expand_group_worker(0x0000ED0F000D1200, 'bitflyer_pubnub_board_diff_',       num_group=2, num_worker=4),
  expand_group_worker(0x0000ED0F000D1300, 'bitflyer_pubnub_ticker_',           num_group=2, num_worker=4),
  expand_group_worker(0x0000ED0F000D1400, 'bitflyer_pubnub_executions_',       num_group=2, num_worker=4),
  expand_group_worker(0x0000ED0F000D1500, 'bitflyer_ws_ticker_board_',         num_group=6, num_worker=4),
        expand_worker(0x0000ED0F000D2000, 'bitflyer_rest_private_',   num_worker=4),
]), check_topic_id_multicastable=True)


if __name__ == '__main__':
  for topic_id, topic_string in sorted(topic_id_to_string_map):
    multicast_addr = topic_id_to_multicast_addr(topic_id)
    print('0x%016X %-23s  %s' % (topic_id, '(%s)' % multicast_addr,
                                 topic_string))
