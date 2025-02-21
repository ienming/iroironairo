/**
 * @author Markus Ekholm
 * @copyright 2012-2023 (c) Markus Ekholm <markus at botten dot org >
 * @license Copyright (c) 2012-2023, Markus Ekholm
 * All rights reserved.
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *    * Redistributions of source code must retain the above copyright
 *      notice, this list of conditions and the following disclaimer.
 *    * Redistributions in binary form must reproduce the above copyright
 *      notice, this list of conditions and the following disclaimer in the
 *      documentation and/or other materials provided with the distribution.
 *    * Neither the name of the author nor the
 *      names of its contributors may be used to endorse or promote products
 *      derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL MARKUS EKHOLM BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */function Z(t,o){o=z(o||{R:255,G:255,B:255}),t=z(t);let n=t;return t.A!==void 0&&(n={R:o.R+(t.R-o.R)*t.A,G:o.G+(t.G-o.G)*t.A,B:o.B+(t.B-o.B)*t.A}),j(y(n))}function y(t){let o=t.R/255,n=t.G/255,s=t.B/255;o>.04045?o=Math.pow((o+.055)/1.055,2.4):o=o/12.92,n>.04045?n=Math.pow((n+.055)/1.055,2.4):n=n/12.92,s>.04045?s=Math.pow((s+.055)/1.055,2.4):s=s/12.92,o*=100,n*=100,s*=100;const e=o*.4124+n*.3576+s*.1805,a=o*.2126+n*.7152+s*.0722,r=o*.0193+n*.1192+s*.9505;return{X:e,Y:a,Z:r}}function j(t){let e=t.Y/100,a=t.Z/108.883,r=t.X/95.047;r>.008856?r=Math.pow(r,1/3):r=7.787*r+16/116,e>.008856?e=Math.pow(e,1/3):e=7.787*e+16/116,a>.008856?a=Math.pow(a,1/3):a=7.787*a+16/116;const h=116*e-16,i=500*(r-e),u=200*(e-a);return{L:h,a:i,b:u}}function z(t){let o,n,s,e;"R"in t?(o=t.R,n=t.G,s=t.B,e=t.A):(o=t.r,n=t.g,s=t.b,e=t.a);const a={R:o,G:n,B:s};return e!==void 0&&(a.A=e),a}/**
 * @author Markus Ekholm
 * @copyright 2012-2023 (c) Markus Ekholm <markus at botten dot org >
 * @license Copyright (c) 2012-2023, Markus Ekholm
 * All rights reserved.
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *    * Redistributions of source code must retain the above copyright
 *      notice, this list of conditions and the following disclaimer.
 *    * Redistributions in binary form must reproduce the above copyright
 *      notice, this list of conditions and the following disclaimer in the
 *      documentation and/or other materials provided with the distribution.
 *    * Neither the name of the author nor the
 *      names of its contributors may be used to endorse or promote products
 *      derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL MARKUS EKHOLM BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */function N(t,o,n){("R"in t||"r"in t)&&(t=Z(t,n)),("R"in o||"r"in o)&&(o=Z(o,n));const s=t.L,e=t.a,a=t.b,r=o.L,h=o.a,i=o.b,u=1,R=1,C=1,l=Math.sqrt(Math.pow(e,2)+Math.pow(a,2)),c=Math.sqrt(Math.pow(h,2)+Math.pow(i,2)),L=(l+c)/2,G=.5*(1-Math.sqrt(Math.pow(L,7)/(Math.pow(L,7)+Math.pow(25,7)))),q=(1+G)*e,B=(1+G)*h,p=Math.sqrt(Math.pow(q,2)+Math.pow(a,2)),d=Math.sqrt(Math.pow(B,2)+Math.pow(i,2)),b=E(a,q),A=E(i,B),k=r-s,X=d-p,m=D(l,c,b,A),g=2*Math.sqrt(p*d)*Math.sin(M(m)/2),H=(s+r)/2,w=(p+d)/2,f=J(l,c,b,A),F=1-.17*Math.cos(M(f-30))+.24*Math.cos(M(2*f))+.32*Math.cos(M(3*f+6))-.2*Math.cos(M(4*f-63)),S=30*Math.exp(-Math.pow((f-275)/25,2)),x=Math.sqrt(Math.pow(w,7)/(Math.pow(w,7)+Math.pow(25,7))),I=1+.015*Math.pow(H-50,2)/Math.sqrt(20+Math.pow(H-50,2)),T=1+.045*w,Y=1+.015*w*F,P=-2*x*Math.sin(M(2*S));return Math.sqrt(Math.pow(k/(I*u),2)+Math.pow(X/(T*R),2)+Math.pow(g/(Y*C),2)+P*(X/(T*R))*(g/(Y*C)))}function v(t){return t*(180/Math.PI)}function M(t){return t*(Math.PI/180)}function E(t,o){if(t===0&&o===0)return 0;{const n=v(Math.atan2(t,o));return n>=0?n:n+360}}function D(t,o,n,s){if(t*o===0)return 0;if(Math.abs(s-n)<=180)return s-n;if(s-n>180)return s-n-360;if(s-n<-180)return s-n+360;throw new Error}function J(t,o,n,s){if(t*o===0)return n+s;if(Math.abs(n-s)<=180)return(n+s)/2;if(Math.abs(n-s)>180&&n+s<360)return(n+s+360)/2;if(Math.abs(n-s)>180&&n+s>=360)return(n+s-360)/2;throw new Error}export{N as c,z as n};
