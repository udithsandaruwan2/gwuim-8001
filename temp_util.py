employee_data = next((item for item in employee_list if item['employee_code'] == data["employee_id"]), None)
        if employee_data['title_uid']:
            title_data = next((item for item in title_list if item['uid'] == employee_data['title_uid']), None)
            schedule_data = next((item for item in employee_work_schedule if item.employee_title_uid == employee_data['title_uid']), None)
            if schedule_data:
                if data["check_in"] and schedule_data.official_start and data["check_in"] > schedule_data.official_start:
                    #late
                    attendance.is_late = True
                    attendance.is_early = False
                    if not schedule_data.relief_start <= data["check_in"] <= schedule_data.relief_end:
                    #late but not also within relief period
                        if schedule_data.late_in_start <= data["check_in"] <= schedule_data.late_in_end:
                        #late but within late in period
                            get_or_create_leave_balance = LeaveBalance.objects.get_or_create(
                                employee_id=employee_data['employee_code'],
                                year=data["date"].year,
                                month=data["date"].month
                            )
                            if get_or_create_leave_balance['late_count'] != 0:
                                get_or_create_leave_balance['late_count'] -= 1
                            elif get_or_create_leave_balance['short_leave_balance'] != 0:
                                get_or_create_leave_balance['short_leave_balance'] -= 1
                                get_or_create_leave_balance['leave_type'] = 'short'
                            else:
                                attendance.is_half_day = True
                                get_or_create_leave_balance['leave_type'] = 'half'
                                get_or_create_leave_balance['half_leave_count'] += 1
                            get_or_create_leave_balance.save()
                        elif schedule_data.short_leave_morning_start <= data["check_in"] <= schedule_data.short_leave_morning_end:
                            #short leave morning
                            attendance.is_short_leave = True
                            get_or_create_leave_balance = LeaveBalance.objects.get_or_create(
                                employee_id=employee_data['employee_code'],
                                year=data["date"].year,
                                month=data["date"].month
                            )
                            if get_or_create_leave_balance['short_leave_balance'] != 0:
                                get_or_create_leave_balance['short_leave_balance'] -= 1
                                get_or_create_leave_balance['leave_type'] = 'short'
                            else:
                                attendance.is_half_day = True
                                get_or_create_leave_balance['leave_type'] = 'half'
                                get_or_create_leave_balance['half_leave_count'] += 1
                            get_or_create_leave_balance.save()
                        elif schedule_data.half_leave_morning_start <= data["check_in"] <= schedule_data.half_leave_morning_end:
                            #half leave morning
                            get_or_create_leave_balance = LeaveBalance.objects.get_or_create(
                                employee_id=employee_data['employee_code'],
                                year=data["date"].year,
                                month=data["date"].month
                                
                            )
                            if get_or_create_leave_balance['half_leave_count'] != 0:
                                get_or_create_leave_balance['half_leave_count'] += 1
                                get_or_create_leave_balance['leave_type'] = 'half'
                            get_or_create_leave_balance.save()
                elif data["check_in"] and schedule_data.late_in_start and data["check_in"] <= schedule_data.late_in_start:
                    #on time
                    attendance.is_late = False
                    attendance.is_early = True
                else:
                    if not data["check_out"] and schedule_data.official_end and data["check_out"] >= schedule_data.official_end:
                        #early leave
                        if schedule_data.short_leave_evening_start <= data["check_out"] <= schedule_data.short_leave_evening_end:
                            #short leave evening
                            attendance.is_short_leave = True
                            get_or_create_leave_balance = LeaveBalance.objects.get_or_create(
                                employee_id=employee_data['employee_code'],
                                year=data["date"].year,
                                month=data["date"].month
                            )
                            if get_or_create_leave_balance['late_count_covered'] < 3 and not get_or_create_leave_balance['late_count_covered'] != 2:
                                get_or_create_leave_balance['late_count_covered'] += 1
                            get_or_create_leave_balance.save()

        # If record already exists, update check-in or check-out