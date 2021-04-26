dr = {
    'review_propreportsdata_random_acc':"SELECT account, ticker FROM public.review_propreportsdata WHERE review_date = date %s AND execution_time >= time %s AND execution_time < time %s ORDER BY random() LIMIT 1",
    'review_datapertickeraccount':"SELECT ticker, total_real, total_shares_traded, session FROM review_datapertickeraccount WHERE account = %s AND review_date = date %s",
    'calc_real_and_shares_amount':"SELECT ticker, sum(real), sum(shares_amount) FROM review_propreportsdata WHERE account = %s AND execution_date = %s AND execution_time >= time %s AND execution_time < time %s GROUP BY ticker",
    'review_dataperticker':'SELECT ticker, result, shares_traded, max_pos, result_in_percents, office_volume, result_in_points, session FROM review_dataperticker WHERE review_date = date %s ORDER BY ticker;',
    'calc_real_shares_max_pos':'SELECT ticker, sum(real::DEC)/10000, sum(shares_amount) FROM review_propreportsdata WHERE execution_date = date %s AND execution_time >= time %s AND execution_time < time %s GROUP BY ticker ORDER BY ticker;'
}