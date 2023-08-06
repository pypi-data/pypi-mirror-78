class API:
    def __init__(self, client):
        self._client = client

    def all_years(self, is_north_hemisphere=None):
        if is_north_hemisphere is None:
            is_north_hemisphere = self._client.user.is_northern_hemisphere

        path = f"/api/year/getall"
        querystring = {"isNorthHemisphere": is_north_hemisphere}
        return self._client._request(
            method="GET", path=path, content_type='json', params=querystring
        )

    def school_by_district(self, district_id=None, school_year_id=None):
        if district_id is None:
            district_id = self._client.preferences.district_id
        if school_year_id is None:
            school_year_id = self._client.preferences.year

        path = f"/api/school/GetByDistrict/{district_id}"
        querystring = {"schoolYearId": school_year_id}
        return self._client._request(
            method="GET", path=path, content_type='json', params=querystring
        )

    def basclass_by_school(self, school_id, school_year_id=None):
        if school_year_id is None:
            school_year_id = self._client.preferences.year

        path = f"/api/class/GetBySchool/{school_id}"
        querystring = {"schoolYearId": school_year_id}
        return self._client._request(
            method="GET", path=path, content_type='json', params=querystring
        )

    def students_by_school_and_school_year(self, school_id, school_year_id=None):
        if school_year_id is None:
            school_year_id = self._client.preferences.year

        path = f"/api/school/GetStudentsBySchoolAndSchoolYear"
        querystring = {"schoolId": school_id, "schoolYear": school_year_id,}
        return self._client._request(
            method="GET", path=path, content_type='json', params=querystring
        )

    def grade_by_school(self, school_id, in_use_only=True):
        path = f"/api/grade/GetBySchool/{school_id}"
        querystring = {"inUseOnly": in_use_only}
        return self._client._request(
            method="GET", path=path, content_type='json', params=querystring
        )

    def student_school_years_and_classes(self, student_id):
        path = f"/api/student/GetStudentSchoolYearsAndClasses"
        querystring = {"studentId": student_id}
        return self._client._request(
            method="GET", path=path, content_type='json', params=querystring
        )
        
    def add_student(self, **kwargs):
        path = f"/api/student/AddStudent"
        payload = dict(
            student=dict(
                firstName=kwargs.get("firstName"),
                lastName=kwargs.get("lastName"),
                studentIdentifier=kwargs.get("studentIdentifier"),
            ),
            studentSchoolYear=dict(
                schoolYearId=kwargs.get("schoolYearId"),
                schoolId=kwargs.get("schoolId"),
                gradeId=kwargs.get("gradeId"),
            ),
            classStudent=dict(
                classId=kwargs.get("classId"),
                fpcclassId=kwargs.get("fpcclassId"),
                groupId=kwargs.get("groupId"),
            ),
        )
        return self._client._request(
            method="POST", path=path, content_type="json", data=payload
        )

    def add_student_to_school_and_grade_and_maybe_class(self, **kwargs):
        path = f"/api/student/AddStudentToSchoolAndGradeAndMaybeClass"
        payload = dict(
            studentId=kwargs.get("studentId"),
            schoolYearId=kwargs.get("schoolYearId"),
            schoolId=kwargs.get("schoolId"),
            gradeId=kwargs.get("gradeId"),
            classStudentStartDate=kwargs.get("classStudentStartDate"),
            classStudentEndDate=kwargs.get("classStudentEndDate"),
            active=kwargs.get("active", True),
            classId=kwargs.get("classId"),
            className=kwargs.get("className"),
            classStartDate=kwargs.get("classStartDate"),
            classEndDate=kwargs.get("classEndDate"),
            schoolLunchProgram=kwargs.get("schoolLunchProgram", False),
            specialEducationServices=kwargs.get("specialEducationServices", False),
            additionalReadingServices=kwargs.get("additionalReadingServices", False),
            otherServicesPrograms=kwargs.get("otherServicesPrograms", False),
            otherServicesDescription=kwargs.get("otherServicesDescription"),
            calendar=dict(
                sortComprehension=kwargs.get("sortComprehension", {}),
                loadingHelper=kwargs.get("loadingHelper", {}),
                isReady=kwargs.get("isReady", True),
                start=kwargs.get("start", {}),
                end=kwargs.get("end", {}),
                holidays=kwargs.get("holidays", []),
            ),
        )
        return self._client._request(
            method="POST", path=path, content_type="json", data=payload
        )
