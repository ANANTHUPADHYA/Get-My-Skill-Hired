export interface ProviderDetails {
    email: string;
    phone: number;
    firstname: string;
    lastname: string;
    address: string;
    area: string;
    city:string;
    price: string;
    days: string[];
    time: string;
    rating: number;
    image:string;
    reviews: string[];
    uuid: string;
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
    city: string;
    customerAddress: string;
    customerNumber: string;
    customerFirstName: string;
    customerLastName: string;
    providerFirstName: string;
    providerLastName: string;
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
    success: boolean;
    data: {
        appointments: Appointment[];
    }
}
    

export interface ReviewParams {
    rating: string;
    review: string;
    
}

export interface ChangeStatusParams {
uuid: string;
appId: string;
status: string;
}

export interface ChangeStatusResponse {
    success: boolean;
    data :{
        message: string;
    }
}

export interface ReviewParams {
    uuid: string;
appId: string;
review: string;
rating: string;
}