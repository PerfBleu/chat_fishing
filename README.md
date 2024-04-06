# 钓鱼
> **这不是一个开箱即用项目。**  
> 你需要有自己的项目，然后将该组件加入到项目中。
>
> `Python 3.10` `APScheduler` `FastAPI`
>
> 该组件由 **服务端** 和 **客户端** 两个部分组成。
> 
> **服务端** 可能需要项目实现一些接口才能正常工作。为了避免提取方法导致的改坏掉，所以是原样上传；**客户端** 是基于 [NoneBot2](https://github.com/nonebot/nonebot2) 和 [OneBot 协议版本 11](https://github.com/botuniverse/onebot-11) 的一种实现。供参考，直接使用或者按需加入到自己的项目中。

一种群聊友好的静默文字游戏。

平台用户通过发送 `开始钓鱼` 开始游戏，期间服务端监听由客户端上报的该用户的所有消息。

每监听到一条消息，都会有一定概率触发鱼咬钩事件，此时根据消息的 **长度** 判断鱼是否上钩或者跑掉。

之后再回到监听状态，并重复该过程，直到平台用户发送 `结束钓鱼` 结束游戏。

用户发送 `结束钓鱼` 后，会返回用户本次钓鱼的结果，包括钓到的鱼的数量和长度记录更新。

用户发送 `钓鱼统计` 可以查看自己的钓鱼统计数据。