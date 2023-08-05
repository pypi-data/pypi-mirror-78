/*! For license information please see main.443adc67.chunk.js.LICENSE.txt */
(this.webpackJsonpstreamlit_custom_tooltip=this.webpackJsonpstreamlit_custom_tooltip||[]).push([[0],{32:function(e,t,n){e.exports=n(43)},43:function(e,t,n){"use strict";n.r(t);var a,r=n(5),s=n.n(r),o=n(16),l=n.n(o),i=n(0),u=n(3),c=n(1),d=n(2),m=n(24),h=n.n(m),E=n(7),g=n(25),f=n(15),p=function(){function e(t,n,a,r){var s=this;Object(i.a)(this,e),this.dataTable=void 0,this.indexTable=void 0,this.columnsTable=void 0,this.styler=void 0,this.getCell=function(e,t){var n=e<s.headerRows&&t<s.headerColumns,a=e>=s.headerRows&&t<s.headerColumns,r=e<s.headerRows&&t>=s.headerColumns;if(n){var o=["blank"];return t>0&&o.push("level"+e),{type:"blank",classNames:o.join(" "),content:""}}if(r){var l=t-s.headerColumns;return{type:"columns",classNames:["col_heading","level"+e,"col"+l].join(" "),content:s.getContent(s.columnsTable,l,e)}}if(a){var i=e-s.headerRows,u=["row_heading","level"+t,"row"+i];return{type:"index",id:"T_".concat(s.uuid,"level").concat(t,"_row").concat(i),classNames:u.join(" "),content:s.getContent(s.indexTable,i,t)}}var c=e-s.headerRows,d=t-s.headerColumns,m=["data","row"+c,"col"+d],h=s.styler?s.getContent(s.styler.displayValuesTable,c,d):s.getContent(s.dataTable,c,d);return{type:"data",id:"T_".concat(s.uuid,"row").concat(c,"_col").concat(d),classNames:m.join(" "),content:h}},this.getContent=function(e,t,n){var a=e.getColumnAt(n);if(null===a)return"";switch(s.getColumnTypeId(e,n)){case f.b.Timestamp:return s.nanosToDate(a.get(t));default:return a.get(t)}},this.dataTable=f.a.from(t),this.indexTable=f.a.from(n),this.columnsTable=f.a.from(a),this.styler=r?{caption:r.get("caption"),displayValuesTable:f.a.from(r.get("displayValues")),styles:r.get("styles"),uuid:r.get("uuid")}:void 0}return Object(u.a)(e,[{key:"getColumnTypeId",value:function(e,t){return e.schema.fields[t].type.typeId}},{key:"nanosToDate",value:function(e){return new Date(e/1e6)}},{key:"rows",get:function(){return this.indexTable.length+this.columnsTable.numCols}},{key:"columns",get:function(){return this.indexTable.numCols+this.columnsTable.length}},{key:"headerRows",get:function(){return this.rows-this.dataRows}},{key:"headerColumns",get:function(){return this.columns-this.dataColumns}},{key:"dataRows",get:function(){return this.dataTable.length}},{key:"dataColumns",get:function(){return this.dataTable.numCols}},{key:"uuid",get:function(){return this.styler&&this.styler.uuid}},{key:"caption",get:function(){return this.styler&&this.styler.caption}},{key:"styles",get:function(){return this.styler&&this.styler.styles}},{key:"table",get:function(){return this.dataTable}},{key:"index",get:function(){return this.indexTable}},{key:"columnTable",get:function(){return this.columnsTable}}]),e}();!function(e){e.COMPONENT_READY="streamlit:componentReady",e.SET_COMPONENT_VALUE="streamlit:setComponentValue",e.SET_FRAME_HEIGHT="streamlit:setFrameHeight"}(a||(a={}));var v=function e(){Object(i.a)(this,e)};v.API_VERSION=1,v.RENDER_EVENT="streamlit:render",v.events=new g.a,v.registeredMessageListener=!1,v.lastFrameHeight=void 0,v.setComponentReady=function(){v.registeredMessageListener||(window.addEventListener("message",v.onMessageEvent),v.registeredMessageListener=!0),v.sendBackMsg(a.COMPONENT_READY,{apiVersion:v.API_VERSION})},v.setFrameHeight=function(e){void 0===e&&(e=document.body.scrollHeight),e!==v.lastFrameHeight&&(v.lastFrameHeight=e,v.sendBackMsg(a.SET_FRAME_HEIGHT,{height:e}))},v.setComponentValue=function(e){v.sendBackMsg(a.SET_COMPONENT_VALUE,{value:e})},v.onMessageEvent=function(e){switch(e.data.type){case v.RENDER_EVENT:v.onRenderMessage(e.data)}},v.onRenderMessage=function(e){var t=e.args;null==t&&(console.error("Got null args in onRenderMessage. This should never happen"),t={});var n=e.dfs&&e.dfs.length>0?v.argsDataframeToObject(e.dfs):{};t=Object(E.a)(Object(E.a)({},t),n);var a=Boolean(e.disabled),r=new CustomEvent(v.RENDER_EVENT,{detail:{disabled:a,args:t}});v.events.dispatchEvent(r)},v.argsDataframeToObject=function(e){var t=e.map((function(e){var t=e.key,n=e.value;return[t,v.toArrowTable(n)]}));return Object.fromEntries(t)},v.toArrowTable=function(e){var t=e.data,n=t.data,a=t.index,r=t.columns;return new p(n,a,r)},v.sendBackMsg=function(e,t){window.parent.postMessage(Object(E.a)({isStreamlitMessage:!0,type:e},t),"*")};s.a.PureComponent;var y=n(53),b=n(8),T=function(e){var t=function(t){Object(c.a)(a,t);var n=Object(d.a)(a);function a(t){var r;return Object(i.a)(this,a),(r=n.call(this,t)).componentDidMount=function(){v.events.addEventListener(v.RENDER_EVENT,r.onRenderEvent),v.setComponentReady()},r.componentDidUpdate=function(){null!=r.state.componentError&&v.setFrameHeight()},r.componentWillUnmount=function(){v.events.removeEventListener(v.RENDER_EVENT,r.onRenderEvent)},r.onRenderEvent=function(e){var t=e;r.setState({renderData:t.detail})},r.render=function(){return null!=r.state.componentError?s.a.createElement("div",null,s.a.createElement("h1",null,"Component Error"),s.a.createElement("span",null,r.state.componentError.message)):null==r.state.renderData?null:s.a.createElement(e,{width:window.innerWidth,disabled:r.state.renderData.disabled,args:r.state.renderData.args})},r.state={renderData:void 0,componentError:void 0},r}return a}(s.a.PureComponent);return t.getDerivedStateFromError=function(e){return{componentError:e}},h()(t,e)}((function(e){var t=e.args,n=(t.label,t.selectedAttributes),a=t.sentence,o={cursor:"pointer",fontSize:"20px"},l={fontSize:"20px"},i={fontSize:"16px"};Object(r.useEffect)((function(){return v.setFrameHeight()}));var u=[],c=JSON.parse(a),d=function(){for(f in h=c[m],E=[],g=[],h)n.includes(f)&&("index"===f?p=h[f]:(E.push(f),g.push(h[f])));var e=[];for(T=E.length,w=0,R=0;R<T;R++)g[R]&&(e.push(s.a.createElement("div",null,E[R],": ",g[R])),w+=1);","===p||"."===p||"?"===p||"!"===p?0===w?u.push(s.a.createElement("a",{style:l},p)):u.push(s.a.createElement(y.a,{content:function(){return s.a.createElement("div",{style:i},e)},placement:b.f.top,returnFocus:!0,autoFocus:!0,showArrow:!0},s.a.createElement("a",{style:o},p))):0===w?(u.push(s.a.createElement("a",{style:l}," ")),u.push(s.a.createElement("a",{style:l},p))):(u.push(s.a.createElement("a",{style:l}," ")),u.push(s.a.createElement(y.a,{content:function(){return s.a.createElement("div",{style:i},e)},placement:b.f.top,returnFocus:!0,autoFocus:!0,showArrow:!0},s.a.createElement("a",{style:o},p))))};for(var m in c){var h,E,g,f,p,T,w,R;d()}return s.a.createElement("div",null,s.a.createElement("div",null," ",u," "),s.a.createElement("br",null),s.a.createElement("br",null),s.a.createElement("br",null),s.a.createElement("br",null))})),w=n(28),R=n(13),C=n(20),_=n(44),N=new w.a;l.a.render(s.a.createElement(s.a.StrictMode,null,s.a.createElement(R.a,{value:N},s.a.createElement(C.b,{theme:_.a},s.a.createElement(T,null)))),document.getElementById("root"))}},[[32,1,2]]]);
//# sourceMappingURL=main.443adc67.chunk.js.map