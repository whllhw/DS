"use strict";
                // Create a new directed graph
var g = new dagreD3.graphlib.Graph().setGraph({});
var Show_Width=document.getElementById("Show").offsetWidth;//为了获取非内嵌div宽度，我花了好长时间啊，最后找到offsetwith可以
var render = new dagreD3.render();
var svg = d3.select('#My_Svg');
var inner = svg.append('g');
var zoom = d3.behavior.zoom().on("zoom", (function() {
            inner.attr("transform", "translate(" + d3.event.translate + ")" +
                         "scale(" + d3.event.scale + ")")}));
svg.call(zoom);
// States and transitions from RFC 793
//先通过 setNode，key定位
var nodes=[{ID:"01",name:"name1",note:"note1"},
    {ID:"02",name:"name2",note:"note2"},
    {ID:"03",name:"name3",note:"note3"},
    {ID:"04",name:"name3",note:"note3"},
    {ID:"05",name:"name3",note:"note3"},
    {ID:"06",name:"name3",note:"note3"},
    {ID:"07",name:"name3",note:"note3"},
    {ID:"08",name:"name3",note:"note3"},
    {ID:"09",name:"name3",note:"note3"}
];
var links=[{head:"01",tail:"02",duration:"6",name:"name1",note:"note1",ES:0,LS:0,Is_Crutical_Path:"1"},
    {head:"01",tail:"03",duration:"4",name:"name2",note:"note2",ES:0,LS:2,Is_Crutical_Path:"0"},
    {head:"01",tail:"04",duration:"5",name:"name2",note:"note2",ES:0,LS:3,Is_Crutical_Path:"0"},
    {head:"02",tail:"05",duration:"1",name:"name2",note:"note2",ES:6,LS:6,Is_Crutical_Path:"1"},
    {head:"03",tail:"05",duration:"1",name:"name2",note:"note2",ES:4,LS:6,Is_Crutical_Path:"0"},
    {head:"04",tail:"06",duration:"2",name:"name2",note:"note2",ES:5,LS:8,Is_Crutical_Path:"0"},
    {head:"05",tail:"07",duration:"9",name:"name2",note:"note2",ES:7,LS:7,Is_Crutical_Path:"1"},
    {head:"05",tail:"08",duration:"7",name:"name2",note:"note2",ES:7,LS:7,Is_Crutical_Path:"1"},
    {head:"06",tail:"08",duration:"4",name:"name2",note:"note2",ES:7,LS:10,Is_Crutical_Path:"0"},
    {head:"07",tail:"09",duration:"2",name:"name2",note:"note2",ES:16,LS:16,Is_Crutical_Path:"1"},
    {head:"08",tail:"09",duration:"4",name:"name2",note:"note2",ES:14,LS:14,Is_Crutical_Path:"1"}
    ];
var nodestates=new Array();
for (var i=0;i<nodes.length;i++)
{
    nodestates[nodes[i].ID]={description:JSON.stringify(nodes[i]),style:"fill:#f77"};
}
var linkstates=new Array();
for (var i=0;i<links.length;i++)
{
    linkstates[i.toString()]={description1:links[i].duration,style:"fill:#f77"};
}
//
// Add states to the graph, set labels, and style
Object.keys(nodestates).forEach(function(state) {//取代hasOwnProperty()的新用法
  var value = nodestates[state];
  value.label = state;
  value.rx = value.ry = 5;
  g.setNode(state, value);
});
// Set up the edges
//画图代码：
for (var i=0;i<links.length;i++)
{
    if(links[i].Is_Crutical_Path=="1")
    {
        g.setEdge(links[i].head,links[i].tail,{label:"dur:"+links[i].duration,style: "stroke: #f66; stroke-width: 3px;",labelStyle: "font-style: italic; text-decoration: underline;"});
        //g.setEdge(links[i].head,links[i].tail,{label:"duration:"+links[i].duration+"\n"+links[i].name+"\n"+links[i].note+"\n"+"\n"+links[i].ES+"|"+links[i].LS,style:"stroke: #f66; stroke-width: 3px; stroke-dasharray: 5, 5;", arrowheadStyle: "fill: #f66" });
    }
    else {
        g.setEdge(links[i].head,links[i].tail,{label:links[i].duration});
    }

}

var styleTooltip = function(name, description) {
return "<p class='name'>" + name + "</p><p class='description'>" + description + "</p>";
};

render(inner,g);

//为元素添加描述
inner.selectAll('g.node')
.attr('title',function(v){return styleTooltip(v, g.node(v).description)})
.each(function(v) { $(this).tipsy({ gravity: "w", opacity: 1, html: true }); });


//
//居中显示
var initialScale = 0.75;
zoom
.translate([(Show_Width - g.graph().width * initialScale) / 2, 20])
.scale(initialScale)
.event(svg);
svg.attr('height', g.graph().height * initialScale + 40);