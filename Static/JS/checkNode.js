//接受数据类型：[[v,w]...[v,w]]
// DFS 判断图是否有环
// 起始节点的数量和终止节点的数量
'use strict';
class checkNode{
	constructor(edges){
		let self = this;
		this.edges = edges;
		this.nodes = new Set();
		for (let edge of edges){
			for (let i of edge){
				this.nodes.add(i);
			}
		}
		this.vexnum = this.nodes.size;
		this.arcnum = edges.length;
		this.vertices = new Array();
		this.nodes.forEach(function(n){
			self.vertices.push(new Vertices(n));
		});
		this.isValid();
	}
	_toAdjacency(){
		let self = this;
		this.edges.forEach(function(edge){
			let i = self._indexOf(edge[0]);
			let j = self._indexOf(edge[1]);
			let pi = new Arcnode(j);
			pi.nextarc = self.vertices[i].firstarc;
			self.vertices[i].firstarc = pi;
		});
	}

	_indexOf(node){
		for(let i = 0;i< this.vexnum ;i++){
			if (node == this.vertices[i].data){
				return i;
			}
		}
		throw "找不到这样的节点" + node;
	}
	_countInDegree(){
		this.inDegerr = new Array(this.vexnum).fill(0);
		for (let edge of this.edges){
			let i = this._indexOf(edge[1]);
			this.inDegerr[i]++;
		}
	}

	_topLogicalSort(){
		let s = new Array();
		for(let i=0;i<this.vexnum;i++){
			if (!this.inDegerr[i]){//放入节点入度为0的点
				s.push(i);
			}
		}
		let count = 0;
		while(s.length){
			let i = s.pop();
			console.log(i,this.vertices[i].data);
			count++;
			for(let p=this.vertices[i].firstarc;p;p=p.nextarc){
				let k = p.adjvex;
				this.inDegerr[k]--;
				if(!this.inDegerr[k]){
					s.push(k);
				}
			}

		}
		if(count<this.vexnum){
			console.log('有回路！！');
			return false;
		}
		return true;
	}


	isValid(){
		this._toAdjacency();
		this._countInDegree();
		return this._topLogicalSort();
	}

}
class Vertices{
	constructor(data){
		this.firstarc = null;
		this.data = data;
	}
}
class Arcnode{
	constructor(data){
		this.adjvex = data;
		this.nextarc = null;
	}
}