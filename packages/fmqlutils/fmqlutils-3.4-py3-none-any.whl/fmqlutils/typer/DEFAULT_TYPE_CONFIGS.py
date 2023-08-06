#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Per (Schema) Type settings for Type Reduction. These may be overridden.

Type Reduction also needs: {SNO}

Companion default 'constants' for typing: 
- period + reductionLabel = "ALL" and countDateType = YEAR
- forceRedo = True
- dataLocationTemplate: "/data/vista/{}/Data/", (as opposed to DataRF for isRF)
"""
TYPE_CONFIGS = {

    "2_98": {
    
        "subTypeProps": ["clinic", "status"],
        
        "createDate": "date_appt_made",
        
        "forceCountProperties": ["scheduling_request_type"]
        
    },
    
    # May add "forceExtension": True ie/ getting duration etc
    "3_081": {
    
        "subTypeProps": ["user", "level_of_assurance", "remote_app", "remote_200_user_ien", "workstation_label", "workstation_type", "remote_station_id", "device"],
            
        "createDate": "date_time",
        
        "forceCountProperties": ["ipv4_address", "remote_station_id", "remote_user_ien"]
        
    },

    "9_7": {

        "createDate": "date_loaded"

    },
    
    "19": {
    
        "subTypeProps": ["type-4"]
        
    },
    
    "26_13": {
    
        "subTypeProps": ["status", "flag_name", "owner_site"]
        
    },

    "26_14": {
            
        "createDate": "date_time",
        
        "subTypeProps": ["action", "entered_by"],
        
        "forceCountPointerTypesExtra": ["8925_1"]
        
    },
    
    "44": {
    
        "subTypeProps": ["stop_code_number", "type_extension", "division"]
        
    },
    
    "44_001": {
    
        "subTypeProps": ["multiple_parent"]
        
    },
    
    "44_003": {

        "createDate": "appointment_date_time",
    
        "isRF": True,
    
        "subTypeProps": ["appointment_container_", "#appointment_cancelled"],
        
        "replyWalkEfficiencyOff": True,

        "note": "efficient walk off as (ala 409_84) [1] using appt start time and not entry time as the create date and [2] this is a flipped multiple"
    
    },

    "45": {
        
        "createDate": "admission_date",
        
        "subTypeProps": ["status", "discharge_status"]
        
    },

    "52": {
            
        "createDate": "login_date",
        
        "subTypeProps": ["status"]
        
    },

    "63_04": {

        "isRF": True,

        "replyWalkEfficiencyOff": True,

        "note": "NOT COMPLETE"

    },

    "74": {
            
        "createDate": "date_report_entered"
        
    },

    "120_5": {
            
        "createDate": "date_time_vitals_taken",
        
        "subTypeProps": ["vital_type", "entered_in_error"]
        
    },

    "120_8": {
        
        "createDate": "origination_date_time",
        
        "subTypeProps": ["gmr_allergy", "entered_in_error"]
        
    },

    "120_86": {
            
        "createDate": "assessment_date_time"
        
    },

    "123": {
            
        "createDate": "file_entry_date",
        
        "subTypeProps": ["cprs_status", "routing_facility", "to_service"]
        
    },

    "221": {
        
        "createDate": "date"
        
    },

    "228_1": {
        
        "createDate": "date_created",

        "subTypeProps": ["location"]
        
    },

    "228_2": {
            
        "createDate": "date"
        
    },
    
    "405": {
    
        "subTypeProps": ["transaction"],
        
        "forceCountProperties": ["roombed", "ward_location"]
        
    },

    "409_68": {
            
        "createDate": "visit_file_entry",
        
        "subTypeProps": ["status"],
        
        "forceCountPointerTypesExtra": ["40_7"],
        
        "replyWalkEfficiencyOff": True
        
    },
    
    "409_831": {
    
        "subTypeProps": ["hospital_location"]
    
    },
    
    "409_833": {
    
        "subTypeProps": ["username"]
        
    },

    "409_84": {
        
        "createDate": "starttime",
        
        "subTypeProps": ["resource", "#cancel_datetime", "#noshow_datetime"],

        "replyWalkEfficiencyOff": True,

        "note": "efficient walk off as using appt start time and not entry time as the create date"
        
    },

    "627_8": {
            
        "createDate": "date_time_of_diagnosis",
        
        "forceCountProperties": ["axis_5"],
        
    },

    "2005": {
        
        "createDate": "date_time_image_saved",
        
        "subTypeProps": ["object_type", "capture_application", "dicom_sop_class", "spec_subspec_index", "status"],
        
        "forceCountProperties": ["group_parent"],
        
        "forceCountPointerTypesExtra": ["71", "2005_81", "2005_82", "2005_83", "2005_84", "2005_85", "2006_04", "2006_81", "8925_1"]
        
    },
    
    "2006_5849": {

        "createDate": "acquisition_start",

        "forceCountProperties": ["consult_audit_trail_transitions"],
    
        "subTypeProps": ["reader_duz_at_acquisition_site", "image_index_for_specialty", "consult_service", "status", "#reading_start"]
        
    },

    "2006_82": {
            
        "createDate": "start",
        
        "subTypeProps": ["start_mode", "workstation"],
        
        "forceCountProperties": ["name"],
        
        "forceCountPointerTypesExtra": ["2006_81"]
        
    },

    "8925": {
            
        "createDate": "entry_date_time",
    
        "subTypeProps": ["document_type", "status"],
        
        "forceCountProperties": ["parent__06_document_type_label"],
        
        "forceCountPointerTypesExtra": ["40_7"]
    
    },
    
    "8989_5": {
    
        "subTypeProps": ["entity"]
        
    },

    "9000010": {
            
        "createDate": "visit_admit_datetime",
        
        # Saw alternative of "service_category", "hospital_location"
        "subTypeProps": ["service_category", "dss_id"],
        
        "forceCountPointerTypesExtra": ["40_7"]
        
    },

    "9000011": {
            
        "createDate": "date_entered",

        "subTypeProps": ["provider_narrative", "condition", "status"],
        
        "forceCountProperties": ["diagnosis", "problem"]
        
    },

    "9000010_11": {
            
        "createDate": "visit",
        
        "subTypeProps": ["immunization", "data_source"]
        
    },

    "9000010_23": {
        
        "createDate": "visit",
        
        "subTypeProps": ["health_factor"],
        
        "forceCountPointerTypesExtra": ["9000010"]
        
    },
    
    "9999999_64": {
    
        "subTypeProps": ["entry_type"]
        
    },
    
    "9000010_99999": {
    
        "isRF": True,
        
        "subTypeProps": ["location"],
        
        "createDate": "date_time_start"
        
    },

    "354_71": {

        "subTypeProps": ["status", "institution"],
        
        "createDate": "date_entry_added"

    }
}
