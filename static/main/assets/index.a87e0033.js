import{g as f,_ as y}from"./index.646dd0dd.js";/* empty css              *//* empty css               *//* empty css              *//* empty css               */import{b4 as I,b5 as v,C as t,D as a,aF as o,G as e,aL as c,aI as i,aH as u,aM as _,aJ as A,b6 as F,aK as n,b7 as S,b8 as x}from"./arco.db8b656f.js";import"./chart.30ec3212.js";import"./vue.d8de27a3.js";const k={name:"Share",data(){return{shareId:"1",loadFinished:!1,shareIdUndefined:!1,user:{username:"admin",avatar:"https://aiclub-1311445709.cos.ap-guangzhou.myqcloud.com/imgbuilder/9/1702750512/tmp/1702750512711.png"},share:{share_type:"sdImage",share_info:'{"image": "https://aiclub-1311445709.cos.ap-guangzhou.myqcloud.com/imgbuilder/15/1706072076/1706072074.png", "params": {"seed": -1, "steps": 20, "width": 512, "height": 512, "prompt": "Spring Festival Authentic Roast Fish Broadcast Activity Package", "cfg_scale": 12, "batch_size": 1, "sampler_name": "Euler a", "negative_prompt": "(worst quality:2),(low quality:2),(normal quality:2),lowres,watermark,"}}'}}},created(){this.getShareInfo()},methods:{getShareInfo(){this.$router.currentRoute.value.query.shareId===void 0?this.shareIdUndefined=!0:(this.shareId=this.$router.currentRoute.value.query.shareId,f(this.shareId).then(r=>{this.user=r.data.user,this.share=r.data.share,this.loadFinished=!0}).catch())}}};const p=r=>(S("data-v-6437ff31"),r=r(),x(),r),b={key:0},N=p(()=>e("header",{class:"user-profile"},[e("h1",{class:"nickname"},"\u5206\u4EAB\u52A0\u8F7D\u5931\u8D25\uFF0C\u8BF7\u68C0\u67E5shareId")],-1)),B=[N],E={key:1,class:"container"},q={class:"user-profile"},w=["src"],C={class:"nickname"},D={class:"content"},J={class:"content-item"},O={key:0},G=["src"],U={key:1},V=["src"],z=p(()=>e("h2",{class:"content-title",style:{"text-align":"center"}},"\u751F\u6210\u6761\u4EF6",-1)),R={class:"conditions-list"},T={key:2},j=["src"];function L(r,M,H,K,s,P){const d=F,h=I,m=v;return t(),a(_,null,[s.shareIdUndefined?(t(),a("div",b,B)):o("",!0),s.loadFinished?(t(),a("div",E,[e("header",q,[e("img",{src:s.user.avatar,alt:"User Avatar",class:"avatar"},null,8,w),e("h1",C,c(s.user.username),1)]),e("section",D,[e("div",J,[s.share.share_type==="mjImage"?(t(),a("div",O,[i(d,{heading:6,style:{"text-align":"center"}},{default:u(()=>[n("\u6765\u81EAMidjourney")]),_:1}),e("img",{src:JSON.parse(s.share.share_info).image,alt:"AI Generated Image",class:"generated-image"},null,8,G),i(h),i(m,{title:"\u63D0\u793A\u8BCD"},{default:u(()=>[n(c(JSON.parse(s.share.share_info).final_prompt),1)]),_:1})])):o("",!0),s.share.share_type==="sdImage"?(t(),a("div",U,[i(d,{heading:6,style:{"text-align":"center"}},{default:u(()=>[n("\u6765\u81EA\u6269\u6563\u6A21\u578B")]),_:1}),e("img",{src:JSON.parse(s.share.share_info).image,alt:"AI Generated Image",class:"generated-image"},null,8,V),i(h),z,e("ul",R,[(t(!0),a(_,null,A(JSON.parse(s.share.share_info).params,(g,l)=>(t(),a("div",{key:l},[e("li",null,[e("strong",null,c(l)+"\uFF1A",1),n(c(g),1)])]))),128))])])):o("",!0),s.share.share_type==="image"?(t(),a("div",T,[i(d,{heading:6,style:{"text-align":"center"}},{default:u(()=>[n("\u6765\u81EA\u7528\u6237")]),_:1}),e("img",{src:JSON.parse(s.share.share_info).image,alt:"AI Generated Image",class:"generated-image"},null,8,j),i(h)])):o("",!0)])])])):o("",!0)],64)}const te=y(k,[["render",L],["__scopeId","data-v-6437ff31"]]);export{te as default};