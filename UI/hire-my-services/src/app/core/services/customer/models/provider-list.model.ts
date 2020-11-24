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
}

export interface ProviderDetailsResponse {
    success: boolean;
    data: {
        providers: ProviderDetails[];
    }
}
    