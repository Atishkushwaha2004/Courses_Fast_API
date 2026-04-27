// static/script.js

const BASE_URL = "";

let allCourses = [];
let currentPage = 1;
const rowsPerPage = 5;

// Load Courses
async function loadCourses(){
    const res = await fetch(`${BASE_URL}/courses`);
    allCourses = await res.json();

    currentPage = 1;
    renderTable();
    updateStats();
}

// Render Table
function renderTable(data = allCourses){

    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;

    const pageData = data.slice(start, end);

    const table = document.getElementById("courseTable");
    table.innerHTML = "";

    pageData.forEach(course => {
        table.innerHTML += `
        <tr>
            <td>${course.id}</td>
            <td>${course.title}</td>
            <td>${course.instructor}</td>
            <td>₹${course.price}</td>
            <td>
              <span class="badge ${course.is_published ? 'published':'draft'}">
                ${course.is_published ? 'Published':'Draft'}
              </span>
            </td>
            <td>
              <button class="btn warning" onclick='editCourse(${JSON.stringify(course)})'>Edit</button>
              <button class="btn danger" onclick="deleteCourse(${course.id})">Delete</button>
            </td>
        </tr>
        `;
    });

    document.getElementById("pageInfo").innerText =
        `Page ${currentPage}`;
}

// Pagination
function nextPage(){
    if(currentPage * rowsPerPage < allCourses.length){
        currentPage++;
        renderTable();
    }
}

function prevPage(){
    if(currentPage > 1){
        currentPage--;
        renderTable();
    }
}

// Stats
function updateStats(){

    const total = allCourses.length;
    const published = allCourses.filter(x => x.is_published).length;
    const draft = total - published;

    const avg = total
      ? Math.round(allCourses.reduce((a,b)=>a+b.price,0)/total)
      : 0;

    totalCourses.innerText = total;
    publishedCourses.innerText = published;
    draftCourses.innerText = draft;
    avgPrice.innerText = `₹${avg}`;
}

// Save
document.getElementById("courseForm").addEventListener("submit", async(e)=>{
    e.preventDefault();

    const id = courseId.value;

    const course = {
        title:title.value,
        instructor:instructor.value,
        category:category.value,
        price:Number(price.value),
        duration_hours:Number(duration_hours.value),
        discount_percent:Number(discount_percent.value),
        is_published:is_published.value === "true"
    };

    if(id){
        await fetch(`${BASE_URL}/courses/${id}`,{
            method:"PUT",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({...course,id:Number(id)})
        });
    }else{
        await fetch(`${BASE_URL}/courses`,{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify(course)
        });
    }

    resetForm();
    loadCourses();
});

// Edit
function editCourse(course){
    courseId.value = course.id;
    title.value = course.title;
    instructor.value = course.instructor;
    category.value = course.category;
    price.value = course.price;
    duration_hours.value = course.duration_hours;
    discount_percent.value = course.discount_percent;
    is_published.value = String(course.is_published);
}

// Delete
async function deleteCourse(id){
    if(confirm("Delete Course?")){
        await fetch(`${BASE_URL}/courses/${id}`,{
            method:"DELETE"
        });
        loadCourses();
    }
}

// Reset
function resetForm(){
    document.getElementById("courseForm").reset();
    courseId.value = "";
}

// Search
function searchCourses(){
    const text = document.getElementById("searchText").value.toLowerCase();

    const filtered = allCourses.filter(course =>
        course.title.toLowerCase().includes(text)
    );

    renderTable(filtered);
}

// Filter by Price
function filterCourses(){

    const max = Number(document.getElementById("maxPrice").value);

    const filtered = allCourses.filter(course =>
        course.price <= max
    );

    renderTable(filtered);
}

loadCourses();