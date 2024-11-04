from django.contrib import admin
from .models import *


class ParticipantAdmin(admin.ModelAdmin): 
  list_display = ('username',
                  'first_name', 
                  'last_name', 
                  'email',
                  'completed_modules',
                  'audio_calibration_float',
                  'behavioral_activated')
  list_filter = ()
admin.site.register(Participant, ParticipantAdmin)


class BehavioralStudyModuleAdmin(admin.ModelAdmin): 
  list_display = ('study_cond',
                  'study_rand_o_1', 
                  'study_rand_o_2')
  list_filter = ()
admin.site.register(BehavioralStudyModule, BehavioralStudyModuleAdmin)


class InterviewAdmin(admin.ModelAdmin):
  list_display = ('participant', 
                  'script_v',
                  'interviewer_summary', 
                  'curr_module_id', 
                  'question_id_count', 
                  'p_notes', 
                  'optional_key_phrases',
                  'completed')
  list_filter = ()
admin.site.register(Interview, InterviewAdmin)


class InterviewModuleAdmin(admin.ModelAdmin): 
  list_display = ('module_id', 
                  'curr_question_id', 
                  'interview', 
                  'completed')
  list_filter = ()
admin.site.register(InterviewModule, InterviewModuleAdmin)


class InterviewQuestionAdmin(admin.ModelAdmin): 
  list_display = ('question_id', 
                  'global_question_id', 
                  'interview', 
                  'module', 
                  'q_content',
                  'q_type',
                  'q_requirement',
                  'q_max_sec',
                  'convo',
                  'completed')
  list_filter = ()
admin.site.register(InterviewQuestion, InterviewQuestionAdmin)


class PerfMeasurementAdmin(admin.ModelAdmin): 
  list_display = ('participant', 
                  'details', 
                  'start_time', 
                  'end_time', 
                  'sec_passed')
  list_filter = ()
admin.site.register(PerfMeasurement, PerfMeasurementAdmin)


class TimeoutTimerAdmin(admin.ModelAdmin): 
  list_display = ('participant',
                  'created', 
                  'endtime',
                  'cause')
  list_filter = ()
admin.site.register(TimeoutTimer, TimeoutTimerAdmin)




