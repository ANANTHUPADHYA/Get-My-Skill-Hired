import { TestBed } from '@angular/core/testing';

import { ProviderListService } from './provider-list.service';

describe('ProviderListService', () => {
  let service: ProviderListService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ProviderListService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
