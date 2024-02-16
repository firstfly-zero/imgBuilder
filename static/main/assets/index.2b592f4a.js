import{_ as k,A as W,B as G,u as H}from"./index.646dd0dd.js";/* empty css              *//* empty css               *//* empty css               */import{d as J,s as K,a as j,g as q,u as P,c as Y}from"./gallery.15a7149f.js";/* empty css               *//* empty css                *//* empty css              *//* empty css               *//* empty css               */import{aY as w,C as m,D as _,aI as t,aH as l,G as r,ae as Z,af as Q,bg as U,bF as X,b1 as V,b7 as $,b8 as ee,a_ as C,aM as E,aJ as D,aE as x,bG as O,bH as z,aK as A,aL as te,aZ as ae,bI as le,bJ as oe,b5 as ne,bd as se,be as ue,bK as ie,bL as de,bh as me,bM as re}from"./arco.db8b656f.js";import"./chart.30ec3212.js";import"./vue.d8de27a3.js";/*! clipboard-copy. MIT License. Feross Aboukhadijeh <https://feross.org/opensource> */var ce=ge;function L(){return new DOMException("The request is not allowed","NotAllowedError")}async function _e(a){if(!navigator.clipboard)throw L();return navigator.clipboard.writeText(a)}async function pe(a){const e=document.createElement("span");e.textContent=a,e.style.whiteSpace="pre",e.style.webkitUserSelect="auto",e.style.userSelect="all",document.body.appendChild(e);const s=window.getSelection(),p=window.document.createRange();s.removeAllRanges(),p.selectNode(e),s.addRange(p);let o=!1;try{o=window.document.execCommand("copy")}finally{s.removeAllRanges(),window.document.body.removeChild(e)}if(!o)throw L()}async function ge(a){try{await _e(a)}catch(e){try{await pe(a)}catch(s){throw s||e||L()}}}const v=ce,be={name:"ImageList",props:["id","url","tag"],emits:["deleteImage"],data(){return{isDeleteImage:!1}},created(){return null},methods:{openDeleteImage(){this.isDeleteImage=!0},deleteImage(a){J(a).then(()=>{this.$emit("deleteImage",a),this.isDeleteImage=!1}).catch()},copyId(a){v(a),w.success("\u56FE\u7247\u94FE\u63A5\u5DF2\u590D\u5236")},shareImage(a){K({share_type:"image",image_url:a}).then(e=>{v(`${window.location.protocol.toString()}//${window.location.host.toString()}/#/share?shareId=${e.data.share_id}`),w.success("\u5206\u4EAB\u94FE\u63A5\u5DF2\u590D\u5236")}).catch(e=>{console.log(e),v("error")})},async onDownLoad(a){await j(a)}}};const Ie=a=>($("data-v-7e8f2ac6"),a=a(),ee(),a),he={class:"card-wrap"},fe={class:"actions"},we=Ie(()=>r("div",null,"\u5220\u9664\u540E\u4E0D\u53EF\u6062\u590D\uFF0C\u786E\u5B9A\u8981\u5220\u9664\u5417\uFF1F",-1));function Fe(a,e,s,p,o,u){const g=W,c=G,b=Z,i=Q,F=U,y=X,h=V;return m(),_("div",he,[t(y,{src:s.url,title:s.tag,width:"260"},{extra:l(()=>[r("div",fe,[t(F,null,{default:l(()=>[r("span",{class:"action",onClick:e[0]||(e[0]=d=>u.shareImage(s.url))},[t(g,{size:"20"})]),r("span",{class:"action",onClick:e[1]||(e[1]=d=>u.onDownLoad(s.url))},[t(c,{size:"20"})]),r("span",{class:"action",onClick:e[2]||(e[2]=d=>u.copyId(s.url))},[t(b,{size:"20"})]),r("span",{class:"action",onClick:e[3]||(e[3]=(...d)=>u.openDeleteImage&&u.openDeleteImage(...d))},[t(i,{size:"20"})])]),_:1})])]),_:1},8,["src","title"]),t(h,{visible:o.isDeleteImage,"onUpdate:visible":e[4]||(e[4]=d=>o.isDeleteImage=d),title:"\u5220\u9664\u56FE\u7247",onOk:e[5]||(e[5]=d=>u.deleteImage(s.id))},{default:l(()=>[we]),_:1},8,["visible"])])}const ye=k(be,[["render",Fe],["__scopeId","data-v-7e8f2ac6"]]),Ae={name:"ImageList",props:["imageList"],components:{ImageWrap:ye},data(){return{}},created(){return null},methods:{deleteImage(a){this.$emit("deleteImage",a)}}};const ve={class:"list-wrap"};function Ce(a,e,s,p,o,u){const g=C("ImageWrap"),c=O,b=z;return m(),_("div",ve,[t(b,{style:{"margin-bottom":"16px"}},{default:l(()=>[(m(!0),_(E,null,D(s.imageList,i=>(m(),x(c,{key:i.id,xs:{span:14,offset:0},sm:{span:10,offset:0},lg:{span:8,offset:0},xl:{span:6,offset:0}},{default:l(()=>[t(g,{id:i.id,height:i.height,width:i.width,tag:i.tag,url:i.url,onDeleteImage:u.deleteImage},null,8,["id","height","width","tag","url","onDeleteImage"])]),_:2},1024))),128))]),_:1})])}const Ee=k(Ae,[["render",Ce],["__scopeId","data-v-e15378c5"]]),De={name:"IbImage",components:{ImageList:Ee},data(){return{galleryId:"1",albumList:[{id:1,album_name:"\u9ED8\u8BA4\u56FE\u5E93-sd",title:"\u9ED8\u8BA4\u56FE\u5E93-sd",desc:"\u9ED8\u8BA4\u56FE\u5E93",image_num:0,status:"public",imageList:[]}],isUploadImage:!1,newImage:{album:"",url:"",height:"",width:"",tag:""},isCreateAlbum:!1,newAlbum:{gallery_id:this.galleryId,album_name:"",title:"",desc:""},headers:{Authorization:`Bearer ${window.localStorage.getItem("token")}`}}},created(){const a=H();this.galleryId=a.galleryId,this.loadData()},methods:{deleteImage(){this.loadData()},loadData(){q(this.galleryId).then(a=>{this.albumList=a.data}).catch()},openUploadImage(){this.isUploadImage=!0},openCreateAlbum(){this.isCreateAlbum=!0},upload_success(a){this.newImage.url=a.response.data.url,this.newImage.height=a.response.data.height,this.newImage.width=a.response.data.width},uploadImage(){P({album_id:this.newImage.album,url:this.newImage.url,height:this.newImage.height,width:this.newImage.width,tag:this.newImage.tag}).then(()=>{this.isUploadImage=!1,w.success("\u56FE\u7247\u4E0A\u4F20\u6210\u529F"),this.loadData()}).catch()},createAlbum(){Y({gallery_id:this.galleryId,album_name:this.newAlbum.album_name,title:this.newAlbum.title,desc:this.newAlbum.desc}).then(()=>{this.isCreateAlbum=!1,w.success("\u76F8\u518C\u521B\u5EFA\u6210\u529F"),this.loadData()}).catch()}}};const xe={class:"container"},ke={style:{"margin-right":"50px"}},Le={style:{"margin-left":"40px","margin-top":"30px"}},Be={style:{"margin-right":"50px"}};function Se(a,e,s,p,o,u){const g=C("Breadcrumb"),c=ae,b=U,i=C("ImageList"),F=le,y=oe,h=O,d=z,M=ne,f=se,I=ue,N=ie,R=de,B=me,T=re,S=V;return m(),_("div",xe,[t(g,{items:["menu.gallery","menu.image"]},null,8,["items"]),t(d,{gutter:20,align:"stretch"},{default:l(()=>[t(h,{span:24},{default:l(()=>[t(M,{class:"general-card",title:"\u56FE\u7247\u5217\u8868"},{extra:l(()=>[t(b,null,{default:l(()=>[t(c,{type:"primary",onClick:u.openCreateAlbum},{default:l(()=>[A("\u65B0\u5EFA\u76F8\u518C")]),_:1},8,["onClick"]),t(c,{type:"primary",onClick:u.openUploadImage},{default:l(()=>[A("\u4E0A\u4F20\u56FE\u7247")]),_:1},8,["onClick"])]),_:1})]),default:l(()=>[t(d,{justify:"space-between"},{default:l(()=>[t(h,{span:24},{default:l(()=>[t(y,{"default-active-tab":1,type:"rounded"},{default:l(()=>[(m(!0),_(E,null,D(o.albumList,n=>(m(),x(F,{key:n.id,title:n.title},{default:l(()=>[t(i,{albumId:n.id,imageList:n.imageList,onDeleteImage:u.deleteImage},null,8,["albumId","imageList","onDeleteImage"])]),_:2},1032,["title"]))),128))]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})]),_:1}),t(S,{visible:o.isUploadImage,"onUpdate:visible":e[2]||(e[2]=n=>o.isUploadImage=n),title:"\u4E0A\u4F20\u56FE\u7247",onOk:u.uploadImage},{default:l(()=>[r("div",ke,[t(B,{model:o.newImage},{default:l(()=>[t(I,{field:"tag",label:"\u6807\u7B7E"},{default:l(()=>[t(f,{modelValue:o.newImage.tag,"onUpdate:modelValue":e[0]||(e[0]=n=>o.newImage.tag=n)},null,8,["modelValue"])]),_:1}),t(I,{field:"album",label:"\u76F8\u518C"},{default:l(()=>[t(R,{modelValue:o.newImage.album,"onUpdate:modelValue":e[1]||(e[1]=n=>o.newImage.album=n)},{default:l(()=>[(m(!0),_(E,null,D(o.albumList,n=>(m(),x(N,{key:n.id,value:n.id},{default:l(()=>[A(te(n.title),1)]),_:2},1032,["value"]))),128))]),_:1},8,["modelValue"])]),_:1})]),_:1},8,["model"]),r("div",Le,[t(T,{draggable:"",action:"/api/v1/gallery/uploadImage","auto-upload":!0,headers:o.headers,onSuccess:u.upload_success},null,8,["headers","onSuccess"])])])]),_:1},8,["visible","onOk"]),t(S,{visible:o.isCreateAlbum,"onUpdate:visible":e[6]||(e[6]=n=>o.isCreateAlbum=n),title:"\u65B0\u5EFA\u76F8\u518C",onOk:u.createAlbum},{default:l(()=>[r("div",Be,[t(B,{model:o.newAlbum},{default:l(()=>[t(I,{field:"album_name",label:"\u76F8\u518C\u540D"},{default:l(()=>[t(f,{modelValue:o.newAlbum.album_name,"onUpdate:modelValue":e[3]||(e[3]=n=>o.newAlbum.album_name=n),placeholder:"\u76F8\u518C\u540D\uFF0C\u56FE\u7247\u4E0A\u4F20\u65F6\u4F7F\u7528"},null,8,["modelValue"])]),_:1}),t(I,{field:"title",label:"\u6807\u9898"},{default:l(()=>[t(f,{modelValue:o.newAlbum.title,"onUpdate:modelValue":e[4]||(e[4]=n=>o.newAlbum.title=n),placeholder:"\u76F8\u518C\u6807\u9898\uFF0C\u540E\u53F0\u5C55\u793A\u65F6\u4F7F\u7528"},null,8,["modelValue"])]),_:1}),t(I,{field:"desc",label:"\u5907\u6CE8"},{default:l(()=>[t(f,{modelValue:o.newAlbum.desc,"onUpdate:modelValue":e[5]||(e[5]=n=>o.newAlbum.desc=n),placeholder:"\u8BF7\u8F93\u5165\u63CF\u8FF0\u4FE1\u606F"},null,8,["modelValue"])]),_:1})]),_:1},8,["model"])])]),_:1},8,["visible","onOk"])])}const je=k(De,[["render",Se],["__scopeId","data-v-f01b3c6e"]]);export{je as default};