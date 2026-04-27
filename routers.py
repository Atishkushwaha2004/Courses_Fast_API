from utils import read_data, save_data, get_next_id
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from pydantic import BaseModel

routers = APIRouter()


# ==============================
# Pydantic Model
# ==============================
class Product(BaseModel):
    id: Optional[int] = None
    title: str
    instructor: str
    category: str
    price: float
    duration_hours: int
    is_published: bool
    discount_percent: float


# ==============================
# Basic Route
# ==============================
@routers.get('/basic-routes')
def show():
    return {'message': "Welcome to FastAPI"}


# ==============================
# GET All Courses
# ==============================
@routers.get('/courses')
def show_courses():
    return read_data()


# ==============================
# GET Course by ID
# ==============================
@routers.get('/courses/{courses_id}')
def show_course_by_id(courses_id: int):

    data = read_data()

    for course in data:
        if int(course['id']) == courses_id:
            return course

    raise HTTPException(
        status_code=404,
        detail=f"Course with ID {courses_id} not found"
    )


# ==============================
# POST - Add Course
# ==============================



@routers.post("/courses")
def add_course(course: dict):

    # data read karo
    data = read_data()

    # auto id generate
    new_id = get_next_id(data)

    # id assign karo
    course["id"] = new_id

    # data me add karo
    data.append(course)

    # file save karo
    save_data(data)

    return {
        "message": "Course added successfully",
        "id": new_id
    }



# ==============================
# PUT - Update Course
# ==============================
@routers.put('/courses/{courses_id}')
def update_data(courses_id: int, update_course: Product):

    data = read_data()

    for index, course in enumerate(data):
        if course['id'] == courses_id:

            updated_dict = update_course.dict()
            updated_dict['id'] = courses_id

            data[index] = updated_dict

            save_data(data)

            return {
                'message': 'Course updated successfully'
            }

    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )


# ==============================
# DELETE - Remove Course
# ==============================
@routers.delete('/courses/{courses_id}')
def remove_courses(courses_id: int):

    data = read_data()

    for index, course in enumerate(data):
        if course.get('id') == courses_id:

            data.pop(index)

            save_data(data)

            return {
                'message': "Course removed successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )


# ==============================
# FILTER Courses
# ==============================
@routers.get('/courses/filter/search')
def filter_courses(
    max_price: Optional[float] = Query(None, description='Maximum Price'),
    is_published: bool = Query(False, description='Show only published courses')
):

    data = read_data()

    if max_price is not None:
        data = [
            course for course in data
            if course['price'] <= max_price
        ]

    if is_published:
        data = [
            course for course in data
            if course.get('is_published')
        ]

    return {
        'total': len(data),
        'courses': data
    }


# ==============================
# PAGINATION
# ==============================
@routers.get('/courses/paginated')
def get_paginated_courses(
    page: int = Query(1, ge=1, description="Page number — starts from 1"),
    page_size: int = Query(5, ge=1, le=50, description="Courses per page")
):

    data = read_data()

    total_courses = len(data)

    # Calculate start and end index
    start = (page - 1) * page_size
    end = start + page_size

    paginated_data = data[start:end]

    # Calculate total pages (ceiling division)
    total_pages = -(-total_courses // page_size)

    # If page does not exist
    if page > total_pages and total_courses > 0:
        raise HTTPException(
            status_code=404,
            detail=f"Page {page} does not exist. Total pages: {total_pages}"
        )

    return {
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
        'total_courses': total_courses,
        'has_next': page < total_pages,
        'has_previous': page > 1,
        'courses': paginated_data
    }





# from utils import read_data, save_data
# from fastapi import APIRouter, HTTPException, Query
# from typing import Optional
# from pydantic import BaseModel

# routers = APIRouter()


# # ==============================
# # Pydantic Model
# # ==============================
# class Product(BaseModel):
#     id: Optional[int] = None
#     title: str
#     instructor: str
#     price: float
#     duration_hours: int
#     is_published: bool
#     discount_percent: float


# # ==============================
# # Basic Route
# # ==============================
# @routers.get('/basic-routes')
# def show():
#     return {'message': "Welcome to FastAPI"}


# # ==============================
# # GET All Courses
# # ==============================
# @routers.get('/courses')
# def show_courses():
#     return read_data()


# # ==============================
# # GET Course by ID
# # ==============================
# @routers.get('/courses/{courses_id}')
# def show_course_by_id(courses_id: int):

#     data = read_data()

#     for course in data:
#         if int(course['id']) == courses_id:
#             return course

#     raise HTTPException(
#         status_code=404,
#         detail=f"Course with ID {courses_id} not found"
#     )


# # ==============================
# # POST - Add Course
# # ==============================
# @routers.post('/courses', status_code=201)
# def add_data(course: Product):

#     data = read_data()

#     # Auto ID generation
#     if data:
#         new_id = max(item['id'] for item in data) + 1
#     else:
#         new_id = 1

#     course_dict = course.dict()
#     course_dict['id'] = new_id

#     data.append(course_dict)

#     save_data(data)

#     return {
#         'message': "Course added successfully",
#         'course_id': new_id
#     }


# # ==============================
# # PUT - Update Course
# # ==============================
# @routers.put('/courses/{courses_id}')
# def update_data(courses_id: int, update_course: Product):

#     data = read_data()

#     for index, course in enumerate(data):
#         if course['id'] == courses_id:

#             updated_dict = update_course.dict()
#             updated_dict['id'] = courses_id

#             data[index] = updated_dict

#             save_data(data)

#             return {
#                 'message': 'Course updated successfully'
#             }

#     raise HTTPException(
#         status_code=404,
#         detail="Course not found"
#     )


# # ==============================
# # DELETE - Remove Course
# # ==============================
# @routers.delete('/courses/{courses_id}')
# def remove_courses(courses_id: int):

#     data = read_data()

#     for index, course in enumerate(data):
#         if course.get('id') == courses_id:

#             data.pop(index)

#             save_data(data)

#             return {
#                 'message': "Course removed successfully"
#             }

#     raise HTTPException(
#         status_code=404,
#         detail="Course not found"
#     )


# # ==============================
# # FILTER Courses
# # ==============================
# @routers.get('/courses/filter/search')
# def filter_courses(
#     max_price: Optional[float] = Query(None, description='Maximum Price'),
#     is_published: bool = Query(False, description='Show only published courses')
# ):

#     data = read_data()

#     if max_price is not None:
#         data = [
#             course for course in data
#             if course['price'] <= max_price
#         ]

#     if is_published:
#         data = [
#             course for course in data
#             if course.get('is_published')
#         ]

#     return {
#         'total': len(data),
#         'courses': data
#     }


# # ==============================
# # PAGINATION
# # ==============================
# @routers.get('/courses/paginated')
# def get_paginated_courses(
#     page: int = Query(1, ge=1, description="Page number — starts from 1"),
#     page_size: int = Query(5, ge=1, le=50, description="Courses per page")
# ):

#     data = read_data()

#     total_courses = len(data)

#     # Calculate start and end index
#     start = (page - 1) * page_size
#     end = start + page_size

#     paginated_data = data[start:end]

#     # Calculate total pages (ceiling division)
#     total_pages = -(-total_courses // page_size)

#     # If page does not exist
#     if page > total_pages and total_courses > 0:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Page {page} does not exist. Total pages: {total_pages}"
#         )

#     return {
#         'page': page,
#         'page_size': page_size,
#         'total_pages': total_pages,
#         'total_courses': total_courses,
#         'has_next': page < total_pages,
#         'has_previous': page > 1,
#         'courses': paginated_data
#     }
