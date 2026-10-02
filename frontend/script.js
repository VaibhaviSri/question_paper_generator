const gen=document.getElementById("gen");

gen.addEventListener("click",makePaper);

async function makePaper(){
    const file=document.getElementById("file").files[0];
    const sub=document.getElementById("sub").value.trim();
    const dur=document.getElementById("dur").value;
    const marks=document.getElementById("marks").value;
    const cnt=document.getElementById("cnt").value;
    const diff=document.getElementById("diff").value;
    const type=document.getElementById("type").value;
    const dist=document.getElementById("dist").value;

    if(!file){
        setStatus("Please upload a syllabus.",true);
        return;
    }

    if(!sub){
        setStatus("Please enter the subject.",true);
        return;
    }

    if(!marks||marks<=0){
        setStatus("Please enter total marks.",true);
        return;
    }

    if(!cnt||cnt<=0){
        setStatus("Please enter the number of questions.",true);
        return;
    }

    const fd=new FormData();

    fd.append("file",file);
    fd.append("sub",sub);
    fd.append("dur",dur);
    fd.append("marks",marks);
    fd.append("cnt",cnt);
    fd.append("diff",diff);
    fd.append("type",type);
    fd.append("dist",dist);

    setStatus("Generating question paper...",false);

    try{
        const res=await fetch("/upload",{
            method:"POST",
            body:fd
        });

        const data=await res.json();

        if(!data.ok){
            setStatus(data.msg,true);
            return;
        }

        showPaper(data);
        setStatus("Question paper generated successfully.",false);
    }catch(err){
        setStatus("Could not connect to the Python backend.",true);
        console.error(err);
    }
}

function showPaper(data){
    const res=document.getElementById("res");
    const qs=data.paper.questions;

    let html=`
        <div class="paper">
            <h2>${data.sub}</h2>
            <p><strong>Duration:</strong> ${data.dur}</p>
            <p><strong>Total Marks:</strong> ${data.marks}</p>
            <hr>
    `;

    qs.forEach((q,i)=>{
        html+=`
            <div class="question">
                <p><strong>Q${i+1}. ${q.question}</strong></p>
                <p>${q.marks} Marks | ${q.type} | ${q.difficulty} | ${q.unit}</p>
            </div>
        `;
    });

    html+=`</div>`;

    res.innerHTML=html;
}

function setStatus(msg,err){
    const status=document.getElementById("status");
    status.textContent=msg;
    status.style.color=err?"red":"green";
}