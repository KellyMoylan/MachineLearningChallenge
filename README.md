# MachineLearningChallenge

Paytm has several merchants who sell merchandise across different categories. As a merchant performance manager I want to understand how well a merchant is doing but since there are so many conflicting dimensions it is hard to say how is merchant performing overall. As an example some merchants may have great service like product they advertise is exactly what they deliver, others may deliver a variation or overpromise to customer. Similarly, a merchant may sell a lot of units but they get ship late consistently and hence cause bad customer experience. 

We want you to come up with a universal score for every merchant to summarize their performance. Think of this as a consumer credit score where many variables are considered and you get positive points for some behaviors and negative for others.


##There are three datasets provided to you –
1.	Transactions – These are all the transactions from users in a fixed time period. This table has merchant id which will let you calculate summary statistics for every merchant.

2.	Profit Metrics–  This dataset has aggregated view of 3 metrics for all merchants-
  a.	Commission%-   Average commission paid by merchant to us, aggregated by primary category.
  b.	Discount %-    Average discount offered by merchant to customers, aggregated by primary category.
  c.	Cash back %-   Average cash back offered by us to customers on items sold by merchant, aggregated by primary category.                       Paytm uses cashback as a preferred method for promotions.

3.	Returned Cancelled Metrics – This dataset has all merchant related cancelled and retuned orders. Merchants sometime cancel the order in case they are not able to acquire inventory or maybe they accepted an order but does not want to ship to a particular pin code. Returns can happen if customer receives order late since merchant did not ship in time or item received is not as promised on the platform. Cancelled and returned order here are only because of merchants’ fault and general customer cancellations are not a part of it.

##Concept of categories 
One thing you will notice in the datasets is category fields T1, T2, T4. All the catalogs are structured in some hierarchy. We have shared 3 levels of hierarchy where T1 -> T2 -> T4 -> Product ID. As an example Mobile and Accessories is a Root category or T1, under this we have 2 Sub categories 1) Mobiles and 2) Accessories and finally each T2 category has many T4 categories (primary category) as an example T2 category Mobiles can have 2 primary categories 1) Smart phones 2) Feature phones. 

##How to complete this challenge:
1.	Fork this repo in github https://github.com/PaytmLabs/MachineLearningChallenge

2.	Complete the processing and analytics as defined first to the best of your ability with the time provided.

3.	Place notes in your code to help with clarity where appropriate. Make it readable enough to present to the Paytm Labs interview team.

4.	Complete your work in your own github repo and send the results to us and/or present them during your interview.

##What is expected:
1.	Provide a list of merchant id and score and explanation of why you think some merchants should have higher score than others.

2.	We expect you to be good in at least 1 programming language. Please don’t complete this using one of the packaged solutions (example SAS)

3.	A good story is as important as an algorithm. We expect you to be able to communicate to us your idea, methodology and implementation. Please provide a 1-page report describing your approach. (Visualizations can be submitted in appendix and are always appreciated but they should convey some message. Interactive visualizations get extra points)

4.	Please make assumptions where necessary, we are interested in approach and if you can defend your assumption we will accept it.













