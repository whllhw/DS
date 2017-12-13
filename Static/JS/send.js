//接受数据类型：
//[{'v':起始节点,'w':下一个节点,'label':描述}...]

class SendEdgeData{
	constructor(data){
		return new SendData(data,'/api/edges').post()
	}
}
//接受数据类型：
//[{'node':节点编号,'name':节点名称,'costTime':耗时}]
class SendNodeData{
	constructor(nodes){
		return new SendData(nodes,'/api/nodes').post()
	}
}

class SendData{
	constructor(data,url,type='add'){
		this.data = {
			data:data,
			length:data.length,
			method:type
		};
		this.url = url;
	}
	post(){
		let msg = null;
		$.ajax({
			type:'POST',
			url:this.url,
			data:JSON.stringify(this.data),
			contentType:'application/json',
			dataType:'json',
			success:function(data){
				msg = data;
				console.log(msg);
			}
		});
		return msg;
	}
}
