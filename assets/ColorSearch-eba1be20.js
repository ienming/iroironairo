import{_ as Q,u as W,i as X,e as d,r as p,I as Y,x as Z,o as ee,a as n,c as r,b as o,t as c,C,n as N,g as h,z as P,T as q,h as B,F as x,l as k,B as oe,E as te,H as f,J as F,m as O,q as le,D as se,p as ae,d as ne}from"./index-55da85dd.js";import{c as re}from"./diff-0ab1811c.js";import{B as ie,N as ce}from"./Navigator-8eee1c28.js";import{I as ue}from"./IroModal-230d99a1.js";import"./Polaroid-8901068a.js";import"./PolaroidText-e9f8eda4.js";const V=_=>(ae("data-v-8feb6097"),_=_(),ne(),_),de={class:"z-1 min-vh-100 bg-silver"},ve={class:"container pt-5 pt-lg-8"},pe={class:"row"},he={class:"sticky-top d-flex flex-column flex-lg-row justify-content-between",style:{top:"30px"}},fe={class:"py-4 py-lg-0"},_e=V(()=>o("h1",{class:"fs-4 ff-serif fw-bolder mb-4"},[o("span",{class:"d-block"},"相近的顏色"),o("span",{class:"fs-6 fw-normal"},"選んだ色に近い色の写真")],-1)),ge={class:"mb-2"},me={class:"bg-white rounded-3 ms-0 shadow-lg overflow-hidden row col-12 col-lg-4"},ye={class:"col-lg-6 py-1 py-lg-3"},be={class:"mb-1"},xe={class:"mb-1"},ke={class:"mb-0"},we={key:0,class:"mt-5 grid-layout"},Se={key:0,class:"position-sticky top-0"},Ie=["src"],Ce={key:0},Ne={class:"random-photo-container"},Pe=["src"],Be={class:"px-4 ps-lg-6 pb-lg-6"},Je={class:"d-flex gap-2 my-2 my-lg-4"},De=["onClick"],Re={class:"txt-lang-container"},He={class:"ps-4 ps-lg-0 pb-8 overflow-x-scroll"},Me=te('<div class="d-flex gap-2 py-4 border-top border-bottom mb-3" data-v-8feb6097><div class="d-flex gap-1 align-items-center" data-v-8feb6097><div style="width:15px;height:15px;" class="rounded-pill bg-dark opacity-25" data-v-8feb6097></div><span data-v-8feb6097>關西地區</span></div><div class="d-flex gap-1 align-items-center" data-v-8feb6097><div style="width:15px;height:15px;" class="bg-dark opacity-25" data-v-8feb6097></div><span data-v-8feb6097>非關西地區</span></div></div>',1),qe={class:"mb-3"},Fe={class:"d-flex py-4 overflow-x-auto"},Oe=["data-place","onClick"],Ve={key:1,class:"row"},$e={class:"col-lg-6 mx-lg-auto mt-6"},ze=V(()=>o("p",{class:"text-center mb-5"}," 找不太到相似顏色的照片，試試搜尋這些顏色？ ",-1)),Ee={class:"d-flex gap-3 justify-content-center"},Le=["onClick"],Te=10,je={__name:"ColorSearch",setup(_){const J=W(),w=X("csvData",[]),v=d(()=>{if(J.query.color)return JSON.parse(J.query.color)}),g=d(()=>{if(v.value)return f(v.value.h,v.value.s,v.value.l)}),m=d(()=>{if(g.value)return F(g.value)});function $(l,t){return re(l,t)}const a=d(()=>{let l=[...w.value];l=l.filter(e=>e.main_color);let t=[];for(let e=0;e<l.length;e++){const s=l[e].colors[0],b=f(s.h,s.s,s.l),U=F(b);$(m.value,U)<Te&&t.push(l[e])}return t=Array.from(new Set(t)),t=t.sort((e,s)=>new Date(e.iso_date.slice(0,-1))-new Date(s.iso_date.slice(0,-1))),t}),S=d(()=>a.value.length>0),I=p(!1),D=p(0),i=d(()=>{if(S.value)return a.value[D.value]});d(()=>{if(i.value)return f(i.value.colors[0].h,i.value.colors[0].s,i.value.colors[0].l)});function R(){if(S.value){I.value=!1;const l=a.value.length-1;D.value=Math.floor(Math.random()*(l+1))}}const z=p(null);function E(){I.value=!0}const L=[{label:"九月 Kugatsu",key:"09"},{label:"十月 Jyuugatsu",key:"10"},{label:"十一月 Jyuuichigatsu",key:"11"},{label:"十二月 Jyuunigatsu",key:"12"},{label:"一月 Ichigatsu",key:"01"},{label:"二月 Nigatsu",key:"02"},{label:"三月 Sangatsu",key:"03"}],y=p(!1),u=p(null);p(null);function H(l){u.value=l,y.value=!0}function T(){const l=e=>e.name===u.value.name,t=a.value.findIndex(l);t>0?a.value[t-1].main_color&&(u.value=a.value[t-1]):u.value=a.value[a.value.length-1]}function j(){const l=e=>e.name===u.value.name,t=a.value.findIndex(l);t==a.value.length-1?u.value=a.value[0]:a.value[t+1].main_color&&(u.value=a.value[t+1])}const G=d(()=>{let l=[];const t=JSON.parse(JSON.stringify(w.value.filter(e=>e.main_color)));if(t.length>0){const e=t.length-1;for(let s=0;s<4;s++){let b=Math.floor(Math.random()*(e+1));l.push(t[b].main_color)}return l}}),M=Y();function A(l){M.push({path:"/color_search",query:{color:JSON.stringify(l)}})}function K(l){M.push({path:"/all",query:{place:JSON.stringify(l)}})}return Z((l,t)=>{y.value=!1}),ee(()=>{window.setInterval(()=>{R()},6e4),R()}),(l,t)=>(n(),r("main",de,[o("div",ve,[o("div",pe,[o("div",he,[o("div",fe,[_e,o("div",ge,[o("span",null,c(a.value.length+"張 / "+C(w).length+"張照片"),1)])]),o("div",me,[o("div",{style:N({"background-color":g.value}),class:"mb-lg-0 col-lg-6 color-searched"},null,4),o("div",ye,[o("p",be,c(g.value),1),o("p",xe,c("RGB: "+m.value.r+", "+m.value.g+", "+m.value.b),1),o("p",ke,c("HSL: "+v.value.h+"o, "+v.value.s+"%, "+v.value.l+"%"),1)])])])])]),S.value?(n(),r("section",we,[o("section",null,[i.value?(n(),r("div",Se,[o("img",{src:i.value.url_google,style:{width:"1px"},class:"position-absolute",onLoad:E},null,40,Ie),h(q,{name:"fade",mode:"out-in"},{default:P(()=>[I.value?(n(),r("section",Ce,[o("div",Ne,[o("img",{ref_key:"randomPhotoEl",ref:z,class:"img-fluid w-100 random-photo",role:"button",src:i.value.url_google,onClick:t[0]||(t[0]=e=>H(i.value))},null,8,Pe)]),o("div",Be,[o("div",Je,[(n(!0),r(x,null,k(i.value.places,e=>(n(),r("div",{key:e.key,class:"px-2 py-1 rounded-pill transition txt-lang-hover bg-dark text-white flex-wrap",role:"button",onClick:s=>K(e)},[o("div",Re,[o("span",null,"#"+c(e),1),o("span",null,"#"+c(e),1)])],8,De))),128))]),o("p",null,c(i.value.description),1)])])):B("",!0)]),_:1})])):B("",!0)]),o("section",He,[o("div",null,[Me,(n(),r(x,null,k(L,e=>o("section",qe,[o("div",{class:O(["d-flex gap-2 ff-serif",a.value.filter(s=>s.date.split("/")[1]==e.key).length>0?"":"opacity-50"])},[o("p",null,[o("strong",null,c(e.label.split(" ")[0]),1),le(" "+c(e.label.split(" ")[1]),1)]),o("span",null,"("+c(a.value.filter(s=>s.date.split("/")[1]==e.key).length)+")",1)],2),o("div",Fe,[(n(!0),r(x,null,k(a.value.filter(s=>s.date.split("/")[1]==e.key),s=>(n(),r("div",{style:N({"background-color":C(f)(s.main_color.h,s.main_color.s,s.main_color.l)}),class:O([s.area=="kansai"?"rounded-pill":"","position-relative color-data flex-shrink-0"]),role:"button","data-place":s.places.length>0?s.places:"無",onClick:b=>H(s)},null,14,Oe))),256))])])),64))])])])):(n(),r("section",Ve,[o("div",$e,[ze,o("div",Ee,[h(oe,{name:"fade"},{default:P(()=>[(n(!0),r(x,null,k(G.value,e=>(n(),r("div",{style:N({"background-color":C(f)(e.h,e.s,e.l)}),class:"rounded-pill color-other",role:"button",key:e.h+e.s+e.l,onClick:s=>A(e)},null,12,Le))),128))]),_:1})])])])),h(q,{name:"fade",mode:"out-in"},{default:P(()=>[y.value?(n(),se(ue,{key:0,photo:u.value,onShowPrev:T,onShowNext:j,onCloseModal:t[1]||(t[1]=e=>y.value=!1)},null,8,["photo"])):B("",!0)]),_:1}),h(ie,{class:"position-fixed top-0 d-flex align-items-center gap-1"}),h(ce)]))}},Xe=Q(je,[["__scopeId","data-v-8feb6097"]]);export{Xe as default};
