/*! For license information please see chunk.0ae0d128973af59bd8fc.js.LICENSE.txt */
(self.webpackJsonp=self.webpackJsonp||[]).push([[158],{210:function(e,t,r){"use strict";function n(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function a(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?a(Object(r),!0).forEach((function(t){n(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):a(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function o(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},i=Object.keys(e);for(n=0;n<i.length;n++)r=i[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(n=0;n<i.length;n++)r=i[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}function l(e,t){return!0===e?[]:!1===e?[t.fail()]:e}r.d(t,"a",(function(){return c})),r.d(t,"b",(function(){return h})),r.d(t,"c",(function(){return f})),r.d(t,"d",(function(){return u})),r.d(t,"e",(function(){return b})),r.d(t,"f",(function(){return v})),r.d(t,"g",(function(){return m})),r.d(t,"h",(function(){return g})),r.d(t,"i",(function(){return x})),r.d(t,"j",(function(){return w})),r.d(t,"k",(function(){return $})),r.d(t,"l",(function(){return O}));class s{constructor(e){const{type:t,schema:r,coercer:n=(e=>e),validator:a=(()=>[]),refiner:i=(()=>[])}=e;this.type=t,this.schema=r,this.coercer=n,this.validator=a,this.refiner=i}}class c extends TypeError{constructor(e,t){const{path:r,value:n,type:a,branch:i}=e,l=o(e,["path","value","type","branch"]);super(`Expected a value of type \`${a}\`${r.length?` for \`${r.join(".")}\``:""} but received \`${JSON.stringify(n)}\`.`),this.value=n,Object.assign(this,l),this.type=a,this.path=r,this.branch=i,this.failures=function*(){yield e,yield*t},this.stack=(new Error).stack,this.__proto__=c.prototype}}function u(e,t){const r=p(e,t);if(r[0])throw r[0]}function d(e,t){const r=t.coercer(e);return u(r,t),r}function p(e,t,r=!1){r&&(e=t.coercer(e));const n=function*e(t,r,n=[],a=[]){const{type:o}=r,s={value:t,type:o,branch:a,path:n,fail:(e={})=>i({value:t,type:o,path:n,branch:[...a,t]},e),check(t,r,i,o){const l=void 0!==i?[...n,o]:n,s=void 0!==i?[...a,i]:a;return e(t,r,l,s)}},c=l(r.validator(t,s),s),[u]=c;u?(yield u,yield*c):yield*l(r.refiner(t,s),s)}(e,t),[a]=n;if(a){return[new c(a,n),void 0]}return[void 0,e]}function h(){return w("any",()=>!0)}function f(e){return new s({type:`Array<${e?e.type:"unknown"}>`,schema:e,coercer:t=>e&&Array.isArray(t)?t.map(t=>d(t,e)):t,*validator(t,r){if(Array.isArray(t)){if(e)for(const[n,a]of t.entries())yield*r.check(a,e,t,n)}else yield r.fail()}})}function b(){return w("boolean",e=>"boolean"==typeof e)}function y(){return w("never",()=>!1)}function v(){return w("number",e=>"number"==typeof e&&!isNaN(e))}function m(e){const t=e?Object.keys(e):[],r=y();return new s({type:e?`Object<{${t.join(",")}}>`:"Object",schema:e||null,coercer:e?j(e):e=>e,*validator(n,a){if("object"==typeof n&&null!=n){if(e){const i=new Set(Object.keys(n));for(const r of t){i.delete(r);const t=e[r],o=n[r];yield*a.check(o,t,n,r)}for(const e of i){const t=n[e];yield*a.check(t,r,n,e)}}}else yield a.fail()}})}function g(e){return new s({type:e.type+"?",schema:e.schema,validator:(t,r)=>void 0===t||r.check(t,e)})}function x(){return w("string",e=>"string"==typeof e)}function w(e,t){return new s({type:e,validator:t,schema:null})}function $(e){const t=Object.keys(e);return w(`Type<{${t.join(",")}}>`,(function*(r,n){if("object"==typeof r&&null!=r)for(const a of t){const t=e[a],i=r[a];yield*n.check(i,t,r,a)}else yield n.fail()}))}function O(e){return w(""+e.map(e=>e.type).join(" | "),(function*(t,r){for(const n of e){const[...e]=r.check(t,n);if(0===e.length)return}yield r.fail()}))}function j(e){const t=Object.keys(e);return r=>{if("object"!=typeof r||null==r)return r;const n={},a=new Set(Object.keys(r));for(const i of t){a.delete(i);const t=e[i],o=r[i];n[i]=d(o,t)}for(const e of a)n[e]=r[e];return n}}},250:function(e,t,r){"use strict";r(5),r(54);var n=r(46),a=r(65),i=r(6),o=r(3),l=r(4);Object(i.a)({_template:l.a`
    <style>
      :host {
        display: inline-block;
        position: relative;
        width: 400px;
        border: 1px solid;
        padding: 2px;
        -moz-appearance: textarea;
        -webkit-appearance: textarea;
        overflow: hidden;
      }

      .mirror-text {
        visibility: hidden;
        word-wrap: break-word;
        @apply --iron-autogrow-textarea;
      }

      .fit {
        @apply --layout-fit;
      }

      textarea {
        position: relative;
        outline: none;
        border: none;
        resize: none;
        background: inherit;
        color: inherit;
        /* see comments in template */
        width: 100%;
        height: 100%;
        font-size: inherit;
        font-family: inherit;
        line-height: inherit;
        text-align: inherit;
        @apply --iron-autogrow-textarea;
      }

      textarea::-webkit-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea::-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-ms-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }
    </style>

    <!-- the mirror sizes the input/textarea so it grows with typing -->
    <!-- use &#160; instead &nbsp; of to allow this element to be used in XHTML -->
    <div id="mirror" class="mirror-text" aria-hidden="true">&nbsp;</div>

    <!-- size the input/textarea with a div, because the textarea has intrinsic size in ff -->
    <div class="textarea-container fit">
      <textarea id="textarea" name\$="[[name]]" aria-label\$="[[label]]" autocomplete\$="[[autocomplete]]" autofocus\$="[[autofocus]]" inputmode\$="[[inputmode]]" placeholder\$="[[placeholder]]" readonly\$="[[readonly]]" required\$="[[required]]" disabled\$="[[disabled]]" rows\$="[[rows]]" minlength\$="[[minlength]]" maxlength\$="[[maxlength]]"></textarea>
    </div>
`,is:"iron-autogrow-textarea",behaviors:[a.a,n.a],properties:{value:{observer:"_valueChanged",type:String,notify:!0},bindValue:{observer:"_bindValueChanged",type:String,notify:!0},rows:{type:Number,value:1,observer:"_updateCached"},maxRows:{type:Number,value:0,observer:"_updateCached"},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,value:!1},inputmode:{type:String},placeholder:{type:String},readonly:{type:String},required:{type:Boolean},minlength:{type:Number},maxlength:{type:Number},label:{type:String}},listeners:{input:"_onInput"},get textarea(){return this.$.textarea},get selectionStart(){return this.$.textarea.selectionStart},get selectionEnd(){return this.$.textarea.selectionEnd},set selectionStart(e){this.$.textarea.selectionStart=e},set selectionEnd(e){this.$.textarea.selectionEnd=e},attached:function(){navigator.userAgent.match(/iP(?:[oa]d|hone)/)&&(this.$.textarea.style.marginLeft="-3px")},validate:function(){var e=this.$.textarea.validity.valid;return e&&(this.required&&""===this.value?e=!1:this.hasValidator()&&(e=a.a.validate.call(this,this.value))),this.invalid=!e,this.fire("iron-input-validate"),e},_bindValueChanged:function(e){this.value=e},_valueChanged:function(e){var t=this.textarea;t&&(t.value!==e&&(t.value=e||0===e?e:""),this.bindValue=e,this.$.mirror.innerHTML=this._valueForMirror(),this.fire("bind-value-changed",{value:this.bindValue}))},_onInput:function(e){var t=Object(o.a)(e).path;this.value=t?t[0].value:e.target.value},_constrain:function(e){var t;for(e=e||[""],t=this.maxRows>0&&e.length>this.maxRows?e.slice(0,this.maxRows):e.slice(0);this.rows>0&&t.length<this.rows;)t.push("");return t.join("<br/>")+"&#160;"},_valueForMirror:function(){var e=this.textarea;if(e)return this.tokens=e&&e.value?e.value.replace(/&/gm,"&amp;").replace(/"/gm,"&quot;").replace(/'/gm,"&#39;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").split("\n"):[""],this._constrain(this.tokens)},_updateCached:function(){this.$.mirror.innerHTML=this._constrain(this.tokens)}});r(140),r(139),r(141);var s=r(64),c=r(121);Object(i.a)({_template:l.a`
    <style>
      :host {
        display: block;
      }

      :host([hidden]) {
        display: none !important;
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container no-label-float$="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">

      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>

      <iron-autogrow-textarea class="paper-input-input" slot="input" id$="[[_inputId]]" aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" bind-value="{{value}}" invalid="{{invalid}}" validator$="[[validator]]" disabled$="[[disabled]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" required$="[[required]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" autocapitalize$="[[autocapitalize]]" rows$="[[rows]]" max-rows$="[[maxRows]]" on-change="_onChange"></iron-autogrow-textarea>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
`,is:"paper-textarea",behaviors:[c.a,s.a],properties:{_ariaLabelledBy:{observer:"_ariaLabelledByChanged",type:String},_ariaDescribedBy:{observer:"_ariaDescribedByChanged",type:String},value:{type:String},rows:{type:Number,value:1},maxRows:{type:Number,value:0}},get selectionStart(){return this.$.input.textarea.selectionStart},set selectionStart(e){this.$.input.textarea.selectionStart=e},get selectionEnd(){return this.$.input.textarea.selectionEnd},set selectionEnd(e){this.$.input.textarea.selectionEnd=e},_ariaLabelledByChanged:function(e){this._focusableElement.setAttribute("aria-labelledby",e)},_ariaDescribedByChanged:function(e){this._focusableElement.setAttribute("aria-describedby",e)},get _focusableElement(){return this.inputElement.textarea}})},374:function(e,t,r){"use strict";r.d(t,"a",(function(){return o}));var n=r(15),a=r(14);const i=new WeakMap,o=Object(a.f)((...e)=>t=>{let r=i.get(t);void 0===r&&(r={lastRenderedIndex:2147483647,values:[]},i.set(t,r));const a=r.values;let o=a.length;r.values=e;for(let i=0;i<e.length&&!(i>r.lastRenderedIndex);i++){const l=e[i];if(Object(n.h)(l)||"function"!=typeof l.then){t.setValue(l),r.lastRenderedIndex=i;break}i<o&&l===a[i]||(r.lastRenderedIndex=2147483647,o=0,Promise.resolve(l).then(e=>{const n=r.values.indexOf(l);n>-1&&n<r.lastRenderedIndex&&(r.lastRenderedIndex=n,t.setValue(e),t.commit())}))}})}}]);
//# sourceMappingURL=chunk.0ae0d128973af59bd8fc.js.map