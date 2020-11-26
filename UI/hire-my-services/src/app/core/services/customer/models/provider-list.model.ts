export interface ProviderDetails {
    email: string;
    phoneNumber: number;
    firstname: string;
    lastname: string;
    address: string;
    area: string;
    city:string;
    skillset: 
    {
    name: string;
    price: number;
    }[];
    days: string[];
    time: string;
    rating: number;
    image:string;
    reviews: {
        comment:string;
    }[];
}

export interface ProviderDetailsResponse {
    success: boolean;
    data: {
        providers: ProviderDetails[];
    }
}

export interface BookAppointmentReq {
    customerEmail: string;
	providerEmail: string;
	date: string;
	time: string;
	serviceType: string;
}

export interface BookAppointmentResp {
    success: boolean;
    data? :{
        message: string;
    };
    error?: {
        message: string;
    };

}

export interface Appointment {
    appointmentID: string;
    appointmentStatus: string;
    customerEmail: string;
    date: string;
    providerEmail: string;
    rating: string;
    review: string;
    serviceType: string;
    time: string;
}

export interface AppointmentList {
    success: boolean
}
    