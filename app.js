const $ = (id) => document.getElementById(id);
let selectedCity = "";
let miniChart, trendChart, barChart;
const chartDefaults = {
  responsive: true, maintainAspectRatio: false,
  plugins: { legend: { labels: { color: "#9aacc4", usePointStyle: true, boxWidth: 7, font: { family: "DM Sans", size: 10 } } } },
  scales: {
    x: { ticks: { color: "#7488a3", maxTicksLimit: 7, font: { size: 9 } }, grid: { color: "#26364a" } },
    y: { ticks: { color: "#7488a3", font: { size: 9 } }, grid: { color: "#26364a" } }
  }
};
function toast(message) { const el=$("toast"); el.textContent=message; el.classList.add("show"); setTimeout(()=>el.classList.remove("show"),3000); }
function notice(message) { const el=$("notice"); el.textContent=message; el.classList.add("show"); setTimeout(()=>el.classList.remove("show"),6000); }
function clearNotice(){ $("notice").classList.remove("show"); }
async function api(url, options={}) {
  const response = await fetch(url, {headers:{"Content-Type":"application/json"}, ...options});
  const data = await response.json().catch(()=>({error:"Unexpected server response."}));
  if(!response.ok) throw new Error(data.error || "Request failed.");
  return data;
}
function weatherSymbol(description="") {
  const d=description.toLowerCase();
  if(d.includes("thunder")) return "ϟ";
  if(d.includes("snow")) return "❄";
  if(d.includes("rain")||d.includes("drizzle")||d.includes("shower")) return "☂";
  if(d.includes("fog")) return "≋";
  if(d.includes("cloud")||d.includes("overcast")) return "☁";
  return "☀";
}
function fmtDate(value) {
  const d=new Date(value.replace(" ","T"));
  return Number.isNaN(d.getTime()) ? value : d.toLocaleString([], {day:"2-digit",month:"short",year:"numeric",hour:"2-digit",minute:"2-digit"});
}
function setCurrent(record) {
  selectedCity=record.city;
  $("current-city").textContent=record.city;
  $("current-country").textContent=record.country || "Current conditions";
  $("current-temp").textContent=Number(record.temperature).toFixed(1);
  $("current-condition").textContent=record.description;
  $("weather-symbol").textContent=weatherSymbol(record.description);
  $("current-time").textContent=fmtDate(record.timestamp);
  $("updated-label").textContent="Saved "+fmtDate(record.timestamp);
  $("hero-humidity").textContent=Number(record.humidity).toFixed(0)+"%";
  $("hero-wind").textContent=Number(record.wind_speed).toFixed(1)+" km/h";
  $("hero-pressure").textContent=Number(record.pressure).toFixed(0)+" hPa";
  $("metric-temp").innerHTML=Number(record.temperature).toFixed(1)+"<small>°C</small>";
  $("metric-humidity").innerHTML=Number(record.humidity).toFixed(0)+"<small>%</small>";
  $("metric-wind").innerHTML=Number(record.wind_speed).toFixed(1)+"<small>km/h</small>";
  $("metric-pressure").innerHTML=Number(record.pressure).toFixed(0)+"<small>hPa</small>";
}
async function searchWeather(city) {
  clearNotice();
  $("search-btn").disabled=true; $("search-btn").textContent="Loading…";
  try {
    const data=await api("/api/weather",{method:"POST",body:JSON.stringify({city})});
    setCurrent(data.record);
    await refreshAll(data.record.city);
    toast(data.message);
  } catch(error) { notice(error.message); }
  finally { $("search-btn").disabled=false; $("search-btn").innerHTML='Search <span>→</span>'; }
}
async function refreshCities() {
  const data=await api("/api/cities");
  ["history-city","analytics-city"].forEach(id=>{
    const select=$(id), previous=select.value;
    select.innerHTML='<option value="">Select a city</option>';
    data.cities.forEach(city=>{const option=document.createElement("option");option.value=city;option.textContent=city;select.appendChild(option);});
    if(data.cities.includes(previous)) select.value=previous;
    else if(selectedCity && data.cities.includes(selectedCity)) select.value=selectedCity;
  });
}
function destroyChart(chart){if(chart)chart.destroy();}
async function loadHistory(city) {
  if(!city){$("history-body").innerHTML='<tr><td colspan="6" class="table-empty">Select a city to see saved readings.</td></tr>';return [];}
  const data=await api("/api/history?city="+encodeURIComponent(city));
  $("history-title").textContent=city+" readings";
  $("history-count").textContent=data.count+" saved observation(s)";
  $("history-body").innerHTML=data.records.length ? data.records.map(r=>`<tr><td>${fmtDate(r.timestamp)}</td><td><b>${Number(r.temperature).toFixed(1)} °C</b></td><td>${Number(r.humidity).toFixed(0)}%</td><td>${Number(r.wind_speed).toFixed(1)} km/h</td><td>${Number(r.pressure).toFixed(0)} hPa</td><td>${escapeHtml(r.description)}</td></tr>`).join("") : '<tr><td colspan="6" class="table-empty">No readings saved for this city.</td></tr>';
  return data.records;
}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
async function loadStats(city) {
  if(!city)return;
  const data=await api("/api/stats?city="+encodeURIComponent(city)), s=data.stats;
  $("analytics-count").textContent=s.count+" saved readings";
  $("stat-high").textContent=Number(s.max_temp).toFixed(1)+"°";
  $("stat-low").textContent=Number(s.min_temp).toFixed(1)+"°";
  $("stat-average").textContent=Number(s.avg_temp).toFixed(1)+"°";
  $("stat-humidity").textContent=Number(s.avg_humidity).toFixed(1)+"%";
  $("stat-high-time").textContent="At "+fmtDate(s.max_time);
  $("stat-low-time").textContent="At "+fmtDate(s.min_time);
}
function makeCharts(records) {
  const ordered=[...records].sort((a,b)=>a.timestamp.localeCompare(b.timestamp));
  const labels=ordered.map(r=>fmtDate(r.timestamp));
  const has=ordered.length>0;
  $("mini-empty").style.display=has?"none":"grid";
  $("trend-empty").style.display=has?"none":"grid";
  $("bar-empty").style.display=has?"none":"grid";
  destroyChart(miniChart);destroyChart(trendChart);destroyChart(barChart);
  if(!has)return;
  miniChart=new Chart($("mini-chart"),{type:"line",data:{labels,datasets:[{label:"Temperature °C",data:ordered.map(r=>r.temperature),borderColor:"#6eafff",backgroundColor:"#6eafff22",fill:true,tension:.35,pointRadius:2}]},options:{...chartDefaults,plugins:{legend:{display:false}}}});
  trendChart=new Chart($("trend-chart"),{type:"line",data:{labels,datasets:[
    {label:"Temperature °C",data:ordered.map(r=>r.temperature),borderColor:"#72b6ff",backgroundColor:"#72b6ff22",yAxisID:"y",tension:.35,pointRadius:3},
    {label:"Humidity %",data:ordered.map(r=>r.humidity),borderColor:"#5dd7c0",backgroundColor:"#5dd7c022",yAxisID:"y1",tension:.35,pointRadius:3}
  ]},options:{...chartDefaults,scales:{...chartDefaults.scales,y:{...chartDefaults.scales.y,position:"left"},y1:{position:"right",min:0,max:100,grid:{drawOnChartArea:false},ticks:{color:"#7488a3"}}}}});
  barChart=new Chart($("bar-chart"),{type:"bar",data:{labels,datasets:[{label:"Temperature °C",data:ordered.map(r=>r.temperature),backgroundColor:"#6eafffbb",borderRadius:5,maxBarThickness:28}]},options:{...chartDefaults,plugins:{legend:{display:false}}}});
}
function renderRecent(records) {
  const latest=[...records].sort((a,b)=>b.timestamp.localeCompare(a.timestamp)).slice(0,4);
  $("recent-list").innerHTML=latest.length?latest.map(r=>`<div class="recent-item"><div><strong>${escapeHtml(r.city)}</strong><small>${fmtDate(r.timestamp)}</small></div><span class="recent-temp">${Number(r.temperature).toFixed(1)}°C</span></div>`).join(""):'<div class="empty-state">No saved readings yet.</div>';
}
async function refreshAll(city=selectedCity) {
  await refreshCities();
  if(!city){const all=await api("/api/history");renderRecent(all.records);return;}
  const records=await api("/api/history?city="+encodeURIComponent(city));
  renderRecent(records.records);makeCharts(records.records);
  $("history-city").value=city;$("analytics-city").value=city;
  try { await loadStats(city); } catch(e) { $("analytics-count").textContent=e.message; }
}
function showView(name) {
  document.querySelectorAll(".view-panel").forEach(el=>el.classList.toggle("active",el.id===name+"-view"));
  document.querySelectorAll(".nav-item").forEach(el=>el.classList.toggle("active",el.dataset.view===name));
  const titles={overview:"Good day",history:"Weather history",analytics:"Weather analytics"};
  $("page-title").textContent=titles[name];
  if(name==="history")loadHistory($("history-city").value).catch(e=>notice(e.message));
  if(name==="analytics")loadAnalytics($("analytics-city").value);
}
async function loadAnalytics(city) {
  if(!city){$("analytics-count").textContent="No city selected";makeCharts([]);return;}
  try {const records=await loadHistoryForCharts(city);await loadStats(city);makeCharts(records);}
  catch(e){$("analytics-count").textContent=e.message;makeCharts([]);}
}
async function loadHistoryForCharts(city){const d=await api("/api/history?city="+encodeURIComponent(city));return d.records;}
document.querySelectorAll(".nav-item").forEach(btn=>btn.addEventListener("click",()=>showView(btn.dataset.view)));
document.querySelectorAll("[data-go]").forEach(btn=>btn.addEventListener("click",()=>showView(btn.dataset.go)));
$("search-form").addEventListener("submit",e=>{e.preventDefault();searchWeather($("city-input").value.trim());});
$("refresh-btn").addEventListener("click",()=>refreshAll().then(()=>toast("Dashboard refreshed." )).catch(e=>notice(e.message)));
$("history-city").addEventListener("change",()=>loadHistory($("history-city").value).catch(e=>notice(e.message)));
$("history-refresh").addEventListener("click",()=>loadHistory($("history-city").value).then(()=>toast("History refreshed.")).catch(e=>notice(e.message)));
$("analytics-city").addEventListener("change",()=>loadAnalytics($("analytics-city").value));
$("export-btn").addEventListener("click",async()=>{try{const response=await fetch("/api/export");if(!response.ok){const d=await response.json();throw new Error(d.error);}const blob=await response.blob();const url=URL.createObjectURL(blob);const a=document.createElement("a");a.href=url;a.download="weather_history.csv";a.click();URL.revokeObjectURL(url);toast("CSV export downloaded.");}catch(e){notice(e.message);}});
$("delete-btn").addEventListener("click",async()=>{const city=$("history-city").value;if(!city){notice("Select a city first.");return;}if(!confirm(`Delete all saved readings for ${city}? This cannot be undone.`))return;try{const d=await api("/api/history/"+encodeURIComponent(city),{method:"DELETE"});toast(d.message);if(selectedCity.toLowerCase()===city.toLowerCase()){selectedCity="";$("current-city").textContent="—";$("current-temp").textContent="--";}await refreshCities();$("history-city").value="";$("history-body").innerHTML='<tr><td colspan="6" class="table-empty">History deleted.</td></tr>';renderRecent([]);makeCharts([]);}catch(e){notice(e.message);}});
$("city-input").addEventListener("input",clearNotice);
$("date-label").textContent=new Date().toLocaleDateString([], {weekday:"long",day:"numeric",month:"long",year:"numeric"}).toUpperCase();
refreshAll().catch(e=>notice("Could not connect to the Flask server. "+e.message));
