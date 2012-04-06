randomwalk <- function(num, source_scale, source_sigma) {
    randy <- c(0,1:num)
    for(i in 2:length(randy)) {
        randy[i] <- source_scale*randy[i-1]+source_sigma*runif(1) 
    }
    return(randy[2:length(randy)])
}

signal <- function(num, source_scale, source_sigma) {
    xs <- sin((1:num)*2*3.14159/360)
    xs <- xs + abs(min(xs)) + 1
    noisy <- source_scale*xs+source_sigma*runif(length(xs))
    return(noisy)
}

received <- function(sent, meas_sigma) {
    measured <- sent+meas_sigma*runif(length(sent))
    return(measured)
}

pred_mean <- function(source_scale, prev_mean) {
    return(source_scale*prev_mean)
}

pred_sigma <- function(source_scale, prev_sigma, source_sigma) {
    return(sqrt((source_scale**2)*(prev_sigma**2)+source_sigma**2))
}

update_mean <- function(pred_mean, pred_sigma, meas_val, meas_sigma) {
    numerator <- (pred_mean/(pred_sigma**2))+(meas_val/(meas_sigma**2))
    denominator <- (1/(pred_sigma**2))+(1/(meas_sigma**2))
    return(numerator/denominator)
}

update_sigma <- function(pred_sigma, meas_sigma) {
    r =(1/(pred_sigma**2))+(1/(meas_sigma**2))
    return(1/sqrt(r))
}

filt <- function(y, source_scale, source_sigma, meas_sigma) {
   last_mean <- 0
   last_sigma <- source_sigma
   k <- 1:length(y)
   for(i in 1:length(y)) {
       est_mean <- pred_mean(source_scale, last_mean)
       est_sigma <- pred_sigma(source_scale, last_sigma, source_sigma)
       k[i] <- est_mean+est_sigma*runif(1)
       last_mean <- update_mean(est_mean, est_sigma, y[i], meas_sigma)
       last_sigma <- update_sigma(est_sigma, meas_sigma)
   }
   return(k)
}

runit <- function() {
    source_sigma <- .2
    source_scale <- sqrt(1-source_sigma**2)
    meas_sigma <- .5
    #x <- signal(1000, source_scale, source_sigma)
    x <- randomwalk(1000, source_scale, source_sigma)
    y <- received(x, meas_sigma)
    k <- filt(y, source_scale, source_sigma, meas_sigma)  
    plot(x, type="l", col="blue")
    lines(k, col="red")
}
