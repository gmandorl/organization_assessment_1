start_time <- Sys.time()

library('ggplot2')
dataset <-'TOOCAN'
days_rm <- 15


plot_time_series <- function(dn, c, x, group, path_fig, label) {

    g <- ggplot(dn,  aes_string(x=x, y=c, group=group)) +
         theme_bw(base_size = 10, base_family = "Times") +
         geom_line(aes_string(color=group), size=0.2) +
         labs( x = x, y = c)

    ggsave( paste(path_fig, label, c, ".png", sep=''), g,
            width=3., height=2.)
}

day_of_year <- function(DN) {
    day_of_year <- DN$day
    delta <- (DN$month>=2)*31  + (DN$month>=3)*28  + (DN$month>=4)*31  + (DN$month>=5)*30 +
             (DN$month>=6)*31  + (DN$month>=7)*30  + (DN$month>=8)*31  + (DN$month>=9)*31 +
             (DN$month>=10)*30 + (DN$month>=11)*31 + (DN$month>=12)*30
    return(day_of_year + delta)
}

month_from_day <- function(DN) {
    month <- 1 + (DN$day_of_year>31)  + (DN$day_of_year>59)  + (DN$day_of_year>90)  + (DN$day_of_year>120) +
                 (DN$day_of_year>151) + (DN$day_of_year>181) + (DN$day_of_year>212) + (DN$day_of_year>243) +
                 (DN$day_of_year>273) + (DN$day_of_year>304) + (DN$day_of_year>334)
}


args = commandArgs(trailingOnly=TRUE)
print ( args[1] )

path <- paste('../organization/output/merged/', dataset,'/', args[1], '/', sep='')

flist <- list.files(path=path)#,  full.names=TRUE)


day_steps   <- seq(0, 23.5, by=0.5)
month_steps <- seq(0, 12,   by=1)


for (fname in flist) {

    dn =  read.csv( paste(path, fname, sep='') )


    DN <- dn#aggregate(dn, by=list(dn$month, dn$day), FUN=mean, na.rm=TRUE)
    DN$day_of_year   <- day_of_year(DN)
#     DN$day_of_year   <- DN$day + (DN$month>=2)*31  + (DN$month>=3)*28  + (DN$month>=4)*31  + (DN$month>=5)*30 +
#                                  (DN$month>=6)*31  + (DN$month>=7)*30  + (DN$month>=8)*31  + (DN$month>=9)*31 +
#                                  (DN$month>=10)*30 + (DN$month>=11)*31 + (DN$month>=12)*30

#     print(head(DN[c('month', 'day', 'day_of_year')],100))

    DN_original <- DN
    for(n in -days_rm:days_rm){
        DN_shifted <- DN_original
        DN_shifted$day_of_year <- sapply(DN_shifted$day_of_year, function(x){x+n})
        DN <- rbind(DN, DN_shifted)
    }

    DN$day_of_year <- DN$day_of_year - 365*(DN$day_of_year>365)
    DN$day_of_year <- DN$day_of_year + 365*(DN$day_of_year<1)
    dn_rm <- aggregate(DN, by=list(DN$day_of_year, DN$hour, DN$minute), FUN=mean, na.rm=TRUE)

    dn_rm$half_hour <- dn_rm$hour + dn_rm$minute/60.
    dn_rm$Group.1 <- NULL
    dn_rm$Group.2 <- NULL
    dn_rm$Group.3 <- NULL
    dn_rm$month   <- month_from_day(dn_rm)
    print(colnames(dn_rm))


    path_out <- paste('output/', dataset, '/', args[1], '/', sep='')
    dir.create(path_out, showWarnings = FALSE, recursive = TRUE)
    write.csv(dn_rm, paste(path_out, 'annualCycle___', fname, sep=''), row.names = FALSE)

    label <- paste(substr(fname, 1, nchar(fname)-4))
    path_out <- paste('figure/', dataset, '/', args[1], '/', label, sep='')
    dir.create(path_out, showWarnings = FALSE, recursive = TRUE)
    path_fig <- paste( path_out, '/', label, sep='')



    dn_month_day <- aggregate(dn, by=list(dn$month, dn$hour), FUN=mean, na.rm=TRUE)



    for (c in colnames(dn)) {
        if(c %in% c("year", "month", "day", "hour", "minute")) {next}


        plot_time_series ( dn_month_day, c,  x="hour",        group="month",      path_fig=path_fig,  label='___hour_'   )
        plot_time_series ( dn_month_day, c,  x="month",       group="hour",       path_fig=path_fig,  label='___month_' )
        plot_time_series ( dn_rm,        c,  x="day_of_year", group="half_hour",  path_fig=path_fig,  label='___day_'     )
        plot_time_series ( dn_rm,        c,  x="half_hour",   group="month",      path_fig=path_fig,  label='___half_hour_'     )


    }

}




print(Sys.time() - start_time)


