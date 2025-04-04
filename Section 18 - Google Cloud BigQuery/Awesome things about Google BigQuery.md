>>> **PROFESSIONAL DATA ENGINEER** - *Google Cloud Platform*
------------------------

> TITLE: "Introduction to Google Cloud - Awesome things about BigQuery"
> 
> Author:
  >- Name: "Vignesh Sekar"
  >- Designation: "Multi Cloud Architect"
  >- Tags: [Google Cloud, DataEngineer, Python, PySpark, SQL, BigData]

-----------------------------------------------------------------------------------------------------------------------

Born out of Dremel in 2012, Google BigQuery is a very unique analytics data warehousing service. BigQuery is often described as serverless, no-ops, seamlessly scalable, and fully managed. Since BigQuery truly has no equivalent, it bears mentioning some of the less obvious aspects of what makes BigQuery so amazing!

**1. Encryption**
BigQuery [(and Google Cloud in general)](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&cd=3&cad=rja&uact=8&ved=0ahUKEwiZ8Jy84uvPAhXhilQKHQzhAVQQFggkMAI&url=https%3A%2F%2Fcloud.google.com%2Fsecurity%2Fencryption-at-rest%2F&usg=AFQjCNHcn98lloEZ-CwUqaD33wNMJCagHQ&sig2=rTtkON_LjpTR7iFefIRgdw&bvm=bv.136499718%2Cd.cGw) takes security very seriously. For example, BigQuery encrypts all data at rest and in transit by default. We believe that encryption is critical to security of all of our customers.

Typical analytics databases suffer a performance hit of 30%-50% associated with encryption. This is important to keep in mind when doing any performance comparisons.

**2. Efficient Concurrency**

Unlike traditional VM-based analytics databases, BigQuery relies on Google-scale sub-services like [Dremel and Colossus for its storage](https://cloud.google.com/blog/big-data/2016/01/bigquery-under-the-hood), compute and memory facilities. All this is tied together by Google’s [Petabit Jupiter Network](https://research.googleblog.com/2015/08/pulling-back-curtain-on-googles-network.html), which essentially allows every node to talk to every other node at 10G.

One of the major benefits of leveraging such an architecture is bottleneck-free scaling and concurrency. Highly optimized cookie-cutter performance benchmarks frequently miss the messy real world, full of unpredictable workloads that compete for common resources and encounter various bottlenecks associated with VM-based architectures.

Allow me to point you to postfrom a team that evaluated BigQuery against a [variety of other technologies,](https://cmtoomey.github.io/speed/2016/11/04/tableaudragrace.html) demonstrating impact of concurrency on real-world use cases.

Moral of the story is that concurrency matters in the real world, and BigQuery’s unique architecture handles concurrency exceptionally well. We encourage you to find out for yourself!

**3. No distribution or sort keys**

BigQuery’s storage is not located on VMs, but rather on a highly performant distributed storage system called Colossus. This lets BigQuery not require any sort or distribution keys whatsoever!

Additional operational overhead aside, databases that require you to define such keys limit your ability to do truly ad-hoc SQL analysis. Queries that suboptimally leverage sort key definitions may perform suboptimally. When looking at performance of such databases, it’s important to measure truly unpredictable queries, rather than queries specifically optimized for sort key definitions.

**4. Ultra-efficient, truly cloud-native pricing**

What if I told you to spin up thousands of servers, install and configure a distributed Big Data service on top of them, load data into the database, run a SQL query, and shut down the whole thing? You’d call me incredibly wasteful. What if I told you that you can do all of the above in 1 second? You’d call me mad. What if I told you that we’ll charge you for the equivalent of per-second billing? You’d call me a liar!

This is exactly what BigQuery’s [on-demand pricing model](https://cloud.google.com/blog/big-data/2016/02/understanding-bigquerys-rapid-scaling-and-simple-pricing) gives you. This is truly [cloud-native and ultra-efficient.](https://cloud.google.com/blog/big-data/2016/02/visualizing-the-mechanics-of-on-demand-pricing-in-big-data-technologies)

This efficiency is especially critical for analytic workloads. 10 years of running Dremel and 5 years of operating BigQuery has shown us that analytic workloads are incredibly volatile. In fact, as demand scales up, analytic workloads get MORE volatile (unlike OLTP).

Therefore, any pricing comparison that models analytic workloads with 0 volatility (or standard deviation) represents highly unrealistic scenarios. Sadly, the real world simply doesn’t work like that.

In other words, BigQuery offers convenience of both real-time bottleneck-free resource allocation (within reason, of course) and assurance of 100% resource utilization. You only pay for what you consume.

By contrast, various industry studies tell us that you’re lucky to run your analytics workload at above 25% utilization, which means that you’re paying 4x what you should be. Some folks even run at [50% utilization by design,](https://www.periscopedata.com/blog/building-the-periscope-cache-with-amazon-redshift.html) purposely doubling their monthly bill.

Of course, there are many reasons to trade cost efficiency for cost predictability, especially in large organizations. For this reason, BigQuery now has Flat Rate Pricing. You pay a flat monthly fee, and all your SQL queries are free. You get the equivalent of a “BigQuery cluster”, except it’s simply a resource config in Dremel, rather than an actual cluster.

**5. Continuously self-optimizing storage**

In March of 2016 BigQuery released [Capacitor](https://cloud.google.com/blog/big-data/2016/04/inside-capacitor-bigquerys-next-generation-columnar-storage-format), a new state-of-the-art storage format and system. One of the many interesting aspects of Capacitor is its opinionated approach to storage. Background processes constantly evaluate customers’ usage patterns, and often automatically optimize these datasets to improve performance. This is entirely automated and transparent for the end user. In practical terms, your queries get faster over time because you’re teaching BigQuery.

In a similar manner, we will never ask you to defrag, vacuum, or re-upload your datasets to BigQuery — this is our idea of fully-managed storage, and we hope that it’s very compelling for our customers.

After 90 days, presumably because we’ve exhausted our capacity to optimize your dataset, we pass on the savings to our customers and automatically drop the price of storage by 50%, without reducing performance or durability.

**6. Highly Available**

BigQuery is highly-available out of the box. All customer data is seamlessly replicated geographically, and our SREs manage where your queries execute. Depending on conditions, you may start the day out in one data center, but seamlessly end up in another a few hours later.

Creating a highly available analytics service is very hard. It requires at least 3x the deployment (and cost) and very non-trivial technical complexity, as [demonstrated](https://aws.amazon.com/blogs/big-data/building-multi-az-or-multi-region-amazon-redshift-clusters/) by this solution.

**7. Caching**

BigQuery offers free per-user cache. If your data doesn’t change, results of your deterministically-written SQL will be automatically cached for 24 hours. Next time you run the same query, your query will execute for free, and your results will be served almost immediately.

Caching is an important consideration when architecting deployments that do periodic refreshes of your SQL queries. If these refreshes hit your cache, you don’t waste any money or resources re-computing what’s already been done. Caching saves money, time, and resources.

**8. Free Batch Ingest**

BigQuery’s batch ingest is a great way to load data into BigQuery. This method is entirely free, or actually mostly amortized into the cost of storage, rather than compute.

Unlike traditional analytics technologies, batch ingest does not consume compute resources from the pool dedicated to analytics and SQL. In other words, no matter how much data you load into BigQuery, your query capacity does not diminish one bit.

Batch ingest is also entirely atomic, which means that jobs either succeed all at once or fail all at once — no nasty race conditions or partial loads to clean up.

**9. Real-time Ingest with Streaming API**

BigQuery’s Streaming API allows you to load up to 100,000 rows per table per second for immediate access in BigQuery. Some customers achieve millions of rows per second by sharding across several tables.

Streaming API does carry its own cost, but, again, traditional analytic data warehouses do not offer free batch or stream ingest, since the cost burden is felt by consumption of paid resources, that are otherwise devoted to SQL.

**10. Serverless, No-ops, and fully-managed**

I’ve previously [opined](https://cloud.google.com/blog/big-data/2016/08/google-bigquery-continues-to-define-what-it-means-to-be-fully-managed) that when it comes to full manageability, BigQuery is in a league of its own — we know when your jobs fail, our SREs are on call 24/7, we seamlessly perform downtime-free upgrades and maintenance, and we will never ever ask you to restart or resize your “BigQuery cluster”.

Finally, BigQuery qualifies to truly be called serverless by every available measure out there.

**11. Easy Data Sharing**

Imagine sharing Petabyte-sized datasets with your coworkers, clients, or partners in the exact same manner you share your Google Spreadsheets and Documents — by keeping the data in place and modifying Access Control Lists (ACLs).

Traditional cloud data warehouses recommend spinning up disparate clusters and loading data into those clusters. This, of course, increases complexity, cost, and operational overhead. BigQuery’s approach is elegant and efficient, and is afforded by BigQuery’s unique serverless architecture.

**12. Public Datasets**

BigQuery takes this “easy data sharing” concept and extends it further. What if ANYONE can access a dataset? Now Terabyte-sized public datasets are immediately available for SQL analysis, without ever so much as spinning up a VM, configuring a database, and loading data into a cluster.

**13. Petabyte-scale**

Would you dare run a full table scan on a Petabyte-sized table? Would you dare to do it live, on-stage, at Strata? Well, BigQuery Product Manager Chad Jennings did exactly that, scanning over a Petabyte in under 4 minutes, demonstrating incredible 4 Terabytes per second throughput.

Some of BigQuery’s largest (external) customers load a Petabyte of data per day and store over a hundred [Petabytes](https://www.oreilly.com/ideas/google-bigquery-for-enterprise) of data in BigQuery.

**14. Federated Access**

Want to query your data in Google Cloud Storage, rather than loading it into BigQuery first? You can do that with BigQuery today. What about query Google Sheets directly from BigQuery? That is also possible. BigQuery offers the [ultra-flexible federated access model](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&cd=1&cad=rja&uact=8&ved=0ahUKEwjMhqPPz-zPAhWIh1QKHaolBEUQFggcMAA&url=https%3A%2F%2Fcloud.google.com%2Fbigquery%2Ffederated-data-sources&usg=AFQjCNFQiWTIaiq9MwFQlb3O5d-6tQN1-A&sig2=icRqdLtT3YCvbOFxvTWUIw&bvm=bv.136499718%2Cd.cGw) for these use cases.

**15. Passionate Customers**

BigQuery’s customers love the service. BigQuery allows them to focus on their business problems and added value, rather than churning complexity and operations.

Some of BigQuery’s customers include [Spotify,](https://news.spotify.com/us/2016/02/23/announcing-spotify-infrastructures-googley-future/) [New York Times,](https://cloud.google.com/blog/big-data/2016/09/bigquery-introducing-powerful-new-enterprise-data-warehousing-features) [Coca Cola,](https://cloud.google.com/blog/big-data/2016/09/bigquery-introducing-powerful-new-enterprise-data-warehousing-features) [Viant,](https://cloud.google.com/blog/big-data/2016/09/bigquery-introducing-powerful-new-enterprise-data-warehousing-features) [Motorola,](https://cloud.google.com/blog/big-data/2016/07/supersize-it-how-motorola-transformed-its-data-warehousing-and-analytics-with-google-cloud-platform) [Kabam Games,](https://youtu.be/6Nv18xmJirs?t=8m) [Vine,](http://stackshare.io/google-bigquery) [Disney Interactive,](https://cloudplatform.googleblog.com/2016/08/the-dragon-days-of-summer-this-week-on-Google-Cloud-Platform.html) [Lloyds Bank,](http://www.ibtimes.co.uk/lloyds-group-partners-google-big-data-analytics-project-understand-customers-1547890) Citigroup, [Sharethis,](https://cloud.google.com/customers/sharethis/) [Wepay,](https://wecode.wepay.com/posts/bigquery-wepay) [Zulily,](https://engineering.zulily.com/2015/08/07/building-zulilys-big-data-platform/) and many many others.

Many of our customers pay nothing or just pennies or dollars per month - after all, you can have as many as 200,000 queries for $5. Many of our customers operate at Petabyte scale. Many of them get to this scale without ever talking to us! And some customers even reach XXX PB scale!


-----------------------------------------------------------------------------------------------------------------------


  <div class="footer">
              copyright © 2022—2023 Cloud & AI Analytics. 
                                      All rights reserved
          </div>