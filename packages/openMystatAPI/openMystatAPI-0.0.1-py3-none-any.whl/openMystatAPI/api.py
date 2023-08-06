import requests


class Api:
    def __init__(self):
        self.api_url = 'https://msapi.itstep.org/api/v2'
        self.application_key = '6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6'


class PublicApi(Api):
    @property
    def all_cities(self):
        method = '/public/cities'
        response = requests.get(f'{self.api_url}{method}')
        return response.json()

    @property
    def all_languages(self):
        method = '/public/languages'
        response = requests.get(f'{self.api_url}{method}')
        return response.json()

    def translation(self, lang=None):
        """
        :param lang: you can get langs from all_languages
        """
        method = '/public/translations'
        response = requests.get(f'{self.api_url}{method}', params={'language': lang})
        return response.json()


class StudentApi(Api):
    def __init__(self, username, password):
        super().__init__()
        self.user_credentials = self.login(username, password).json()
        self.access_token = self.user_credentials['access_token']
        self.auth_headers = {'Authorization': f'Bearer {self.access_token}'}

    def api_request(self, method, url_method='GET', data=None, params=None):
        response = requests.request(url=f'{self.api_url}{method}',
                                    method=url_method,
                                    headers=self.auth_headers,
                                    data=data,
                                    params=params
                                    )
        return response

    def login(self, username, password):
        method = '/auth/login'
        response = requests.post(f'{self.api_url}{method}',
                                 data={'username': username,
                                       'password': password,
                                       'application_key': self.application_key}
                                 )
        self.user_credentials = response.json()
        return response

    @property
    def student_achievements(self):
        method = '/profile/statistic/student-achievements'
        return self.api_request(method).json()

    def materials_list(self, material_type):
        method = '/profile/statistic/student-achievements'
        return self.api_request(method, params={'material_type': material_type}).json()

    @property
    def leader_group_points(self):
        method = '/dashboard/progress/leader-group-points'
        return self.api_request(method).json()

    @property
    def leader_group(self):
        method = '/dashboard/progress/leader-group'
        return self.api_request(method).json()

    @property
    def leader_stream_points(self):
        method = '/dashboard/progress/leader-stream-points'
        return self.api_request(method).json()

    @property
    def leader_stream(self):
        method = '/dashboard/progress/leader-stream'
        return self.api_request(method).json()

    @property
    def study_activity_log(self):
        method = '/dashboard/progress/activity'
        return self.api_request(method).json()

    @property
    def counter_homework(self):
        method = '/count/homework'
        return self.api_request(method).json()

    @property
    def average_progress_chart(self):
        method = '/dashboard/chart/average-progress'
        return self.api_request(method).json()

    @property
    def attendance_chart(self):
        method = '/dashboard/chart/attendance'
        return self.api_request(method).json()

    @property
    def future_exams(self):
        method = '/dashboard/info/future-exams'
        return self.api_request(method).json()

    @property
    def user_info(self):
        method = '/settings/user-info'
        return self.api_request(method).json()

    @property
    def evaluation_list(self):
        method = '/feedback/students/evaluate-lesson-list'
        return self.api_request(method).json()

    @property
    def city_contacts(self):
        method = '/contacts/operations/index'
        return self.api_request(method).json()

    @property
    def student_visits(self):
        method = '/progress/operations/student-visits'
        return self.api_request(method).json()

    @property
    def exams(self):
        method = '/progress/operations/student-exams'
        return self.api_request(method).json()

    @property
    def study_plan_url(self):
        method = '/progress/operations/plan-url'
        return self.api_request(method).json()

    @property
    def progress_chart(self):
        method = '/dashboard/chart/progress'
        return self.api_request(method).json()

    @property
    def history_specs(self):
        method = '/settings/history-specs'
        return self.api_request(method).json()

    @property
    def group_specs(self):
        method = '/settings/group-specs'
        return self.api_request(method).json()

    @property
    def group_history(self):
        method = '/homework/settings/group-history'
        return self.api_request(method).json()

    @property
    def homework_list(self):
        method = '/homework/operations/list'
        return self.api_request(method).json()

    def schedule_month(self, date_filter=None):
        method = '/schedule/operations/get-month'
        return self.api_request(method, params={'date_filter': date_filter}).json()

    def schedule_date(self, date_filter=None):
        method = '/schedule/operations/get-by-date'
        return self.api_request(method, params={'date_filter': date_filter}).json()

    def month_events(self, date_filter=None):
        method = '/schedule/operations/month-events'
        return self.api_request(method, params={'date_filter': date_filter}).json()

    def products_list(self, page=1, product_type=0):
        method = '/market/customer/product/list'
        return self.api_request(method, params={'page': page, 'type': product_type}).json()

    def pushchased_list(self, page=1):
        method = '/market/customer/order/list'
        return self.api_request(method, params={'page': page}).json()

    def pushchased_info(self, product_id=0):
        method = '/market/customer/order/info'
        return self.api_request(method, params={'id': product_id}).json()

    @property
    def signal_problems_list(self):
        method = '/signal/operations/problems-list'
        return self.api_request(method).json()

    @property
    def signals_list(self):
        method = '/signal/operations/signals-list'
        return self.api_request(method).json()

    def signals_comments(self, signal_id=0):
        method = '/signal/operations/signals-comments'
        return self.api_request(method, params={'id': signal_id}).json()

    @property
    def unread_signals(self):
        method = '/signal/operations/count-unread'
        return self.api_request(method).json()

    def signal_reference_data(self, reference_type=0):
        method = '/signal/operations/get-reference-data'
        return self.api_request(method, params={'type': reference_type}).json()

    @property
    def signal_reference_status(self):
        method = '/signal/operations/get-reference-status'
        return self.api_request(method).text

    @property
    def student_itstep_feedbacks(self):
        method = '/feedback/social-review/get-review-list'
        return self.api_request(method).json()

    @property
    def itstep_reviewing_instruction(self):
        method = '/reviews/index/instruction'
        return self.api_request(method).json()

    @property
    def profile_data(self):
        method = '/profile/operations/settings'
        return self.api_request(method).json()

    def send_sms(self):
        method = '/contacts/sms/send-code'
        return self.api_request(method, url_method='POST').json()

    @property
    def recomendations_list(self):
        method = '/referral/operations/list'
        return self.api_request(method).json()

    @property
    def payment_info(self):
        method = '/payment/operations/index'
        return self.api_request(method).json()

    @property
    def payment_plan(self):
        method = '/payment/operations/schedule'
        return self.api_request(method).json()

    @property
    def payment_history(self):
        method = '/payment/operations/history'
        return self.api_request(method).json()

    @property
    def opened_interview(self):
        method = '/library/quiz/opened-interview'
        return self.api_request(method).text

    @property
    def latest_news(self):
        method = '/news/operations/latest-news'
        return self.api_request(method).text

    def news_info(self, news_id=0):
        method = '/news/operations/detail-news'
        return self.api_request(method, params={'news_id': news_id}).json()

    @property
    def unread_news(self):
        method = '/news/operations/count-unread'
        return self.api_request(method).json()
