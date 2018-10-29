create table if not exists toplist(
    live    varchar(10),  
    client  varchar(100),
    device  varchar(100),
    topplat varchar(100),
    newsid  varchar(100), --新闻ID
    title   text,        ---标题
    postdate    varchar(100),  ---发布时间
    orderdate   varchar(100),
    description text,      ----描述
    image   varchar(500),  ----图片
    hitcount    varchar(100),  ----点击次数
    commentcount    varchar(100),  ----评论数
    cid varchar(100),
    sid varchar(100),
    url varchar(200),    ----文章链接
    insert_time datetime  ----爬取时间
);

create table if not exists newslist(
    newsid    text(10),  --新闻ID
    title   text,  ---标题
    v   text,
    orderdate varchar(100),
    postdate    varchar(100), ---发布时间
    description text, ---描述
    image   varchar(500),  ----图片
    slink   varchar(500), ---超链
    hitcount    varchar(100),  ---点击次数
    commentcount    varchar(100),  ---评论数
    cid varchar(100),   
    url varchar(200),  ---文章链接
    live varchar(100),
    lapinid varchar(100),  ----辣品id
    forbidcomment   varchar(100),
    imagelist text,    ---图片列表
    c   varchar(500),
    client  varchar(100),
    isad    varchar(10),
    sid varchar(100),
    PostDateStr varchar(100),
    HitCountStr varchar(200),
    WapNewsUrl  varchar(200),
    TipClass    varchar(100),
    TipName varchar(100),
    insert_time datetime
)

create table if not exists newsdetail(
    newsid    varchar(10),
    title   text,
    keywords   text,
    description text,
    types varchar(100),
    news_author varchar(100),
    detail text,
    duty_man varchar(100),
    insert_time datetime
)


create table if not exists newscomment(
    newsid    varchar(10),
    l   varchar(100),
    comment_id  varchar(100),
    comment mediumtext,
    nick_name   varchar(100),
    userid  varchar(100),
    user_location   varchar(100),
    comment_time    varchar(100),
    support varchar(100),
    disagree  varchar(100),
    device_name  varchar(100),
    r   varchar(100),
    clientid    varchar(100),
    ir  varchar(100),        ----是否是it之家小编
    sf  varchar(100),
    user_level  varchar(100),
    tl  varchar(100),
    rl  varchar(100),
    reply_userid    varchar(100),
    m   varchar(100),
    headimg varchar(200),
    writetime   varchar(100),
    clientname  varchar(100),
    userindexurl    varchar(200),
    insert_time datetime	
) DEFAULT CHARSET=utf8mb4

create table if not exists newscomment_re(
    newsid    varchar(10),
)