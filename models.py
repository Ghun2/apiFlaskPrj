# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, ForeignKeyConstraint, Index, Integer, String, Text, Time
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
Base = declarative_base()


class CategoryLaw(db.Model):
    __tablename__ = 'CategoryLaw'

    law_id = db.Column(db.Integer, primary_key=True)
    applied_date = db.Column(db.DateTime)
    minimum_wage = db.Column(db.Integer)
    law_02 = db.Column(db.Integer)
    law_03 = db.Column(db.Integer)
    created_time = db.Column(db.String(45), server_default=db.FetchedValue())
    updated_time = db.Column(db.String(45))


class Daily(db.Model):
    __tablename__ = 'Daily'

    daliy_id = db.Column(db.Integer, primary_key=True, nullable=False)
    tc_id = db.Column(db.ForeignKey('timecard.tc_id'), index=True)
    wcond_id = db.Column(db.ForeignKey('workcondition.wcond_id'), nullable=False, index=True)
    target_ym = db.Column(db.String(6), primary_key=True, nullable=False)
    target_date = db.Column(db.String(2), primary_key=True, nullable=False)
    work_start = db.Column(db.DateTime)
    work_end = db.Column(db.DateTime)
    rest_start = db.Column(db.DateTime)
    rest_end = db.Column(db.DateTime)
    actual_worktime = db.Column(db.Time)
    contract_worktime = db.Column(db.Time)
    over_worktime = db.Column(db.Time)
    night_worktime = db.Column(db.Time)
    actual_dailypay = db.Column(db.Integer)
    contract_dailypay = db.Column(db.Integer)
    minimum_dailypay = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime)

    tc = db.relationship('Timecard', primaryjoin='Daily.tc_id == Timecard.tc_id', backref='dailies')
    wcond = db.relationship('Workcondition', primaryjoin='Daily.wcond_id == Workcondition.wcond_id', backref='dailies')


class FAQ(db.Model):
    __tablename__ = 'FAQ'

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Integer)
    sequence = db.Column(db.Integer)
    level = db.Column(db.Integer)
    title = db.Column(db.String(45))
    content = db.Column(db.Text)
    active = db.Column(db.Integer)
    created_time = db.Column(db.String(45))
    updated_time = db.Column(db.String(45))


class Monthly(db.Model):
    __tablename__ = 'Monthly'

    monthly_id = db.Column(db.Integer, primary_key=True)
    wcond_id = db.Column(db.ForeignKey('workcondition.wcond_id'), nullable=False, index=True)
    create_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    update_time = db.Column(db.DateTime)

    wcond = db.relationship('Workcondition', primaryjoin='Monthly.wcond_id == Workcondition.wcond_id', backref='monthlies')


class TermsAgreement(db.Model):
    __tablename__ = 'TermsAgreement'

    terms_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    terms_01 = db.Column(db.Integer)
    terms_02 = db.Column(db.Integer)
    terms_03 = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime)


class TimeCard(db.Model):
    __tablename__ = 'TimeCard'

    tc_id = db.Column(db.Integer, primary_key=True, nullable=False)
    wcond_id = db.Column(db.ForeignKey('workcondition.wcond_id'), nullable=False, index=True)
    target_ym = db.Column(db.String(6), primary_key=True, nullable=False)
    target_date = db.Column(db.String(2), primary_key=True, nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    rest_start_time = db.Column(db.DateTime)
    rest_end_time = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime)

    wcond = db.relationship('Workcondition', primaryjoin='TimeCard.wcond_id == Workcondition.wcond_id', backref='time_cards')


class TimeCardMemo(db.Model):
    __tablename__ = 'TimeCardMemo'
    __table_args__ = (
        db.ForeignKeyConstraint(['tc_id', 'target_ym', 'target_date'], ['timecard.tc_id', 'timecard.target_ym', 'timecard.target_date']),
        db.Index('fk_TimeCardMemo_TimeCard1_idx', 'tc_id', 'target_ym', 'target_date')
    )

    tcmemo_id = db.Column(db.Integer, primary_key=True)
    tc_id = db.Column(db.Integer, nullable=False)
    target_ym = db.Column(db.String(6), nullable=False)
    target_date = db.Column(db.String(2), nullable=False)
    article = db.Column(db.Text)
    having_photo = db.Column(db.String(255))
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime)

    tc = db.relationship('Timecard', primaryjoin='and_(TimeCardMemo.tc_id == Timecard.tc_id, TimeCardMemo.target_ym == Timecard.target_ym, TimeCardMemo.target_date == Timecard.target_date)', backref='time_card_memos')


class User(Base):
    __tablename__ = 'User'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(16))
    email = db.Column(db.String(255))
    birth = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    password = db.Column(db.String(32))
    user_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime)


class WorkCondition(db.Model):
    __tablename__ = 'WorkCondition'

    wcond_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.user_id'), nullable=False, index=True)
    wp_id = db.Column(db.ForeignKey('workplace.wp_id'), nullable=False, index=True)
    cont_id = db.Column(db.ForeignKey('workcontract.cont_id'), index=True)
    start_work_date = db.Column(db.String(8))
    start_work_time = db.Column(db.Time)
    end_work_time = db.Column(db.Time)
    start_rest_time = db.Column(db.Time)
    end_rest_time = db.Column(db.Time)
    amount_work_time = db.Column(db.Time)
    amount_rest_time = db.Column(db.Time)
    hourly_pay = db.Column(db.Integer)
    monthly_pay = db.Column(db.Integer)
    payday = db.Column(db.String(4))
    pay_type = db.Column(db.String(45))
    wcond_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime)

    cont = db.relationship('Workcontract', primaryjoin='WorkCondition.cont_id == Workcontract.cont_id', backref='work_conditions')
    user = db.relationship('User', primaryjoin='WorkCondition.user_id == User.user_id', backref='work_conditions')
    wp = db.relationship('Workplace', primaryjoin='WorkCondition.wp_id == Workplace.wp_id', backref='work_conditions')


class WorkContract(db.Model):
    __tablename__ = 'WorkContract'

    cont_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.user_id'), nullable=False, index=True)
    wp_id = db.Column(db.ForeignKey('workplace.wp_id'), nullable=False, index=True)
    contract_01 = db.Column(db.Integer)
    contract_02 = db.Column(db.Integer)
    contract_03 = db.Column(db.Integer)
    contract_04 = db.Column(db.Integer)
    contract_05 = db.Column(db.Integer)
    cont_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    having_photo = db.Column(db.String(255))
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime)

    user = db.relationship('User', primaryjoin='WorkContract.user_id == User.user_id', backref='work_contracts')
    wp = db.relationship('Workplace', primaryjoin='WorkContract.wp_id == Workplace.wp_id', backref='work_contracts')


class WorkPlace(db.Model):
    __tablename__ = 'WorkPlace'

    wp_id = db.Column(db.Integer, primary_key=True)
    wp_name = db.Column(db.String(45))
    address = db.Column(db.String(255))
    kakao_place_id = db.Column(db.String(45))
    road_address = db.Column(db.String(255))
    category_name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    bjd_code = db.Column(db.String(10))
    building_name = db.Column(db.String(255))
    business_code = db.Column(db.String(45))
    owner = db.Column(db.String(45))
    over_5employee = db.Column(db.Integer, server_default=db.FetchedValue())
    x = db.Column(db.Text)
    y = db.Column(db.Text)
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime)


class Yearly(db.Model):
    __tablename__ = 'Yearly'

    yearly_id = db.Column(db.Integer, primary_key=True)
    wcond_id = db.Column(db.ForeignKey('workcondition.wcond_id'), nullable=False, index=True)
    create_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    update_time = db.Column(db.DateTime)

    wcond = db.relationship('Workcondition', primaryjoin='Yearly.wcond_id == Workcondition.wcond_id', backref='yearlies')


class Timecard(db.Model):
    __tablename__ = 'timecard'

    tc_id = db.Column(db.Integer, primary_key=True, nullable=False)
    wcond_id = db.Column(db.ForeignKey('workcondition.wcond_id'), nullable=False, index=True)
    target_ym = db.Column(db.String(6), primary_key=True, nullable=False)
    target_date = db.Column(db.String(2), primary_key=True, nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    rest_start_time = db.Column(db.DateTime)
    rest_end_time = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime)

    wcond = db.relationship('Workcondition', primaryjoin='Timecard.wcond_id == Workcondition.wcond_id', backref='timecards')


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(16))
    email = db.Column(db.String(255))
    birth = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    password = db.Column(db.String(32))
    user_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime)


class Workcondition(db.Model):
    __tablename__ = 'workcondition'

    wcond_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.user_id'), nullable=False, index=True)
    wp_id = db.Column(db.ForeignKey('workplace.wp_id'), nullable=False, index=True)
    cont_id = db.Column(db.ForeignKey('workcontract.cont_id'), index=True)
    start_work_date = db.Column(db.String(8))
    start_work_time = db.Column(db.Time)
    end_work_time = db.Column(db.Time)
    start_rest_time = db.Column(db.Time)
    end_rest_time = db.Column(db.Time)
    amount_work_time = db.Column(db.Time)
    amount_rest_time = db.Column(db.Time)
    hourly_pay = db.Column(db.Integer)
    monthly_pay = db.Column(db.Integer)
    payday = db.Column(db.String(4))
    pay_type = db.Column(db.String(45))
    wcond_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime)

    cont = db.relationship('Workcontract', primaryjoin='Workcondition.cont_id == Workcontract.cont_id', backref='workconditions')
    user = db.relationship('User', primaryjoin='Workcondition.user_id == User.user_id', backref='workconditions')
    wp = db.relationship('Workplace', primaryjoin='Workcondition.wp_id == Workplace.wp_id', backref='workconditions')


class Workcontract(db.Model):
    __tablename__ = 'workcontract'

    cont_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.user_id'), nullable=False, index=True)
    wp_id = db.Column(db.ForeignKey('workplace.wp_id'), nullable=False, index=True)
    contract_01 = db.Column(db.Integer)
    contract_02 = db.Column(db.Integer)
    contract_03 = db.Column(db.Integer)
    contract_04 = db.Column(db.Integer)
    contract_05 = db.Column(db.Integer)
    cont_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    having_photo = db.Column(db.String(255))
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime)

    user = db.relationship('User', primaryjoin='Workcontract.user_id == User.user_id', backref='workcontracts')
    wp = db.relationship('Workplace', primaryjoin='Workcontract.wp_id == Workplace.wp_id', backref='workcontracts')


class Workplace(db.Model):
    __tablename__ = 'workplace'

    wp_id = db.Column(db.Integer, primary_key=True)
    wp_name = db.Column(db.String(45))
    address = db.Column(db.String(255))
    kakao_place_id = db.Column(db.String(45))
    road_address = db.Column(db.String(255))
    category_name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    bjd_code = db.Column(db.String(10))
    building_name = db.Column(db.String(255))
    business_code = db.Column(db.String(45))
    owner = db.Column(db.String(45))
    over_5employee = db.Column(db.Integer, server_default=db.FetchedValue())
    x = db.Column(db.Text)
    y = db.Column(db.Text)
    created_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime)
