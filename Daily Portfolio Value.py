def compute_daily_portfolio_val( prices, alloc, start_val):

    
    normed = prices/prices.ix[0]
   
    alloced = normed * alloc
    
    pos_val = alloced * start_val
   
    port_val = pos_val.sum(axis = 1)
     
    return port_val
