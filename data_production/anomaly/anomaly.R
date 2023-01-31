start_time <- Sys.time()


day_of_year <- function(DN) {
    day_of_year <- DN$day
    delta <- (DN$month>=2)*31  + (DN$month>=3)*28  + (DN$month>=4)*31  + (DN$month>=5)*30 +
             (DN$month>=6)*31  + (DN$month>=7)*30  + (DN$month>=8)*31  + (DN$month>=9)*31 +
             (DN$month>=10)*30 + (DN$month>=11)*31 + (DN$month>=12)*30
    return(day_of_year + delta)
}


dataset<-'TOOCAN'
args = commandArgs(trailingOnly=TRUE)
print ( args[1] )

path_data  <- paste('../organization/output/merged/', dataset, '/', args[1], '/', sep='')
path_cycle <- paste('output/', dataset, '/', args[1], '/', sep='')
flist <- list.files(path=path_data)

if (args[1]=='P2'){
    if (args[2]=='1') { flist = flist[1:15] }
    if (args[2]=='2') { flist = flist[15:length(flist)] }
}


hour_steps    <- seq(0, 23)
minute_steps  <- c(0, 30)
day_of_year_steps   <- seq(1, 365)





for (fname in flist) {
    print(fname)

    fname_cycles <- paste(args[1], '_base.csv', sep='')
    if ( grepl( 'F', args[1], fixed = TRUE) ) {
        fname_cycles <- fname
        print(fname_cycles)
        }
    dn              <- read.csv( paste(path_data, fname, sep='') )
    dn_annual_cycle <- read.csv( paste(path_cycle, 'annualCycleFit___', fname_cycles, sep='') )
#     dn_annual_cycle =  read.csv( paste(path_cycle, 'annualCycle___', fname, sep='') )

    dn$day_of_year   <- day_of_year(dn)

    dn_anomly <- data.frame(matrix(ncol = ncol(dn), nrow = 0))

    #provide column names
    colnames(dn_anomly) <- colnames(dn)
    dn_anomly_to_copy <- dn_anomly


    for(h in hour_steps) {
      for(m in minute_steps) {
        for(d in day_of_year_steps) {
#             print('')
#             print(h)
#             print(m)
#             print(d)

            dn_anomly_tmp      <- subset(dn,              (hour == h & minute == m & day_of_year == d))
            annual_mean        <- subset(dn_annual_cycle, (hour == h & minute == m & day_of_year == d))
            if(nrow(annual_mean)>1) {print('ERROR! More than one value in the annual mean')}

            for (c in colnames(dn_anomly)) {
                if(c %in% c("year", "month", "day", "hour", "minute", "day_of_year")) {next}


                dn_anomly_tmp[[c]] <- sapply(dn_anomly_tmp[[c]], function(x, y){x-y}, y=annual_mean[[c]])
            }
            dn_anomly <- rbind(dn_anomly_tmp, dn_anomly)

        }
      }
    }

    dn_anomly = dn_anomly[with(dn_anomly, order(year, month, day, hour, minute)),]
    print(head(dn_anomly))
    write.csv(dn_anomly, paste(path_cycle, 'anomaly___', fname, sep=''), row.names = FALSE)


}

print(Sys.time() - start_time)
