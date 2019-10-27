import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdUploaderComponent } from './ad-uploader.component';

describe('AdUploaderComponent', () => {
  let component: AdUploaderComponent;
  let fixture: ComponentFixture<AdUploaderComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdUploaderComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdUploaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
