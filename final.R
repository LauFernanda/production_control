y <-read.table("./data_final.txt")

y1<-as.numeric(y[,1])

plot.ts(y1)

acf2(y)

ydiff<-diff(y1,differences = 2)

plot.ts(ydiff)

acf2(ydiff)

library(forecast)
fit <- Arima(ydiff, order=c(1,0,1))
summary(fit)
(1-pnorm(abs(fit$coef)/sqrt(diag(fit$var.coef))))*2 #p valores de la estimaci?

Acf(residuals(fit))
acf2(residuals(fit))

plot(forecast(fit, h = 100))

plot(y, type="l", col = "red")
plot(residuals(fit))

r<- residuals(fit)
# Q-Q plots
.pardefault <- par()
par(mfrow=c(1,2))

# normal fit 
qqnorm(r); qqline(r)

# t(3Df) fit 
qqplot(rnorm(1000, mean=mean(r), sd = sd(r)), r, main="Normal Q-Q Plot", 
       ylab="Sample Quantiles")
abline(0,1)
par(.pardefault)

hist(residuals(fit))

plot(y,type="l", xlab="Periods")
lines(y-residuals(fit), type="o", col = "red")
legend(600,10,  c("Y(t)","ARIMA(2,0,1)"), lty=c(1,1), lwd=c(2.5,2.5),col=c("black","red")) 

