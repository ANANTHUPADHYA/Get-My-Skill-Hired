
export  interface LoginResponse {
        status: number; 
        success: boolean;
        data: {
            accessToken: string;
            profile: {
                userType: string;
                uuid: string; 
                username: string; 
                email: string;
                firstName: string; 
                lastName: string;
                phone: string;
                address: string; 
                city: string;
                days?: string[];
                time?: string;
                skillset?: 
                    {
                        name: string;
                        price: number;
                    }[]
                
            }
        }
  }
  
  export interface UserParams {
      firstName: string;
      lastName: string;
      address: string;
      area: string;
      city: string;
      phone: string;
      userType: string;
      days?: string[];
      time?: string;
      skillSet?: {
          name: string;
          price: number;
      }[]
  }
  
  export interface RegisterResponse {
    success: boolean;
    data?: string;
    
    
  }
  
  