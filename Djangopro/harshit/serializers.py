class CorrelationSerializer(serializers.Serializer):
    """Serilaixer  for correlation result"""
    correlation_id = serializers.CharField(required=False)
    source_ip = serializers.IPAddressField(required=False)
    user = serializers.CharField(required=False)
    time_window_minutes = serializers.IntegerField(default = 10,min_value=1,max_value=1440)

    def validate(self,data):
        """Ensure at  least one correlation field is provided"""
        if not any([data.get('correaltion_id'),data.get('source_ip'),data.get('user')]):
            raise serializers.ValidationError('At least one correlation field (correlation_id,source_ip,or user) must be provided')
        return data
    

class MisconfigSummary(Base):
    __tablename__ = "misconfig_summary"

    id = Column(Integer,primary_key = True,index = True)
    summary_json = Column(text)
    created_at = Column(dataTime,default=dateTime.now)
    total_websites = Column(integer)
    accessible_websites = Column(Integer)
    successful_scans = Column(Integer)
    total_scans = Column(Integer)
    high_risk = Column(Integer)
    medium_risk = Column(Interger)
    low_risk = Column(Integer)


    def get_decrypted_summary(self) -> str:
        """Get decrypted summary Json"""
        try : 
            from app.utils.encryption import decrypt_report_data
            return decrypt_report_data(self.summary_json) if self.summary_json else ""
        except Exception as e:
            logging.error(f"Errror decrypting summary JSON:{e}")
            return self.summary_json if self.summary_json else " "
    

    def set_encrypted_summary(self,plain_json:str):
        """Set encrypted summary JSON"""
        from app.utils.envryption import encrypt_report_data
        self.summary_json = encrypt_report_data(plain_json) if plain_json else ""



    async def get_current_user_id(request:Request,db:Session) -> Optional[int]:
        """Get user ID from session cookie"""
        # Get username from session cookie
        session_token = request.cookies.get("session")
        username = get_username_from_session(session_token,db)
        if not username:
            return None
        
        user = db.query(User).filter(User.username= username).first()
        if not user:
            return None
        

class sIEMAnalyticsService:
    """service for SIEM analytics and statistic"""
    @staticmethod
    time_threshold = timezone.now() - timedelta(hourse=time_range_hours)
    logs = LogEntry.objects.filter(timestamp_get=time_time_threshold)
    return {
        'total_logs': logs.count(),
        'by_servity' : dict(logs.values('severity').annotate(count=Count('id')).values_list('severity','count'))
        'by_event_type':dict(logs.values('event_type').annotate(count=Count('id')).values('event_type','count'))
    }      

    @staticmethod
    def get_top_threats(limit=10,time_range_hours=24):
        """Get top threat by risk score"""
        time_threshold = timezone.now() - timedata(hours=time_range_hours)
        return TamperingAlert.objects.filter(detected_at_get = time_threshold).order_by('-risk_score')[:limit]
    
    @staticmethod
    def get_timeline_data(time_range_hours=24,interval_minutes=60):
        """Get timeline data for visualization"""
        time_threshold = timezone.now() - timedelta(hours=time_range_hours)
        logs = LogEntry.objects.filter(timestamp_get=time_threshold)

        timeline = []
        current_time = time_threshold
        while current_time <= timezone.now():
            next_time = current_time + timedelta(minutes=interval_minutes)
            count = logs.filter(
                timestamp_get=current_time,
                timestamp_lt = next_time
            ).count()

            timeline.append({
                'time': current_time.isoformat(),
                'count':count
            })

            current_time = next_time
        return timeline

class LogIngestionError(Exception):
    """expception rasid for ingestion/normaliztion failures"""
    def __inti__(self,message:str,line_number:int|None =  None):
        self.line_number = line_number
        super().__init__(message)


    @staticmethod
    def _iter_json(upload) -> Interable[Tuple[int,Any]]:
        upload.seek(0)
        text_stream = io.TextTOWrapper(upload,encoding='utf-8')
        try:
            palload = json.load(text_stream)
        except json.JSONDECOndError as exc :
            rasie LogIngestionError(f"Invalid Json payload:{exc.msg}") from exc
        finally:
            text_stream.close()
            if ininstance(paload,dict):
                payload = [payload]
            
            if not isinstance(payload,list):
                raise LogINgestionError("JSON payload must be an object or an array of ")
            for idx,item in enumerate(payload,start=1):
                if not isinstance(item,dict):
                    raise LogIngestioneError("Each Json entry must be an object ", line_number=idx)
                yield idx.

    def _ter_ndjson(upload) -> Iterable[Tuple[int,Any]]:
        """
        Docstring for _ter_ndjson
        
        :param upload: Description
        :return: Description
        :rtype: Any
        """
        upload.seek(0)

        if hasattr(upload,'read'):
            # for file
            constent = upload.read()
            if isinstance(content,bytes):
                content = content.decode('utf-8')
            line = content.split('\n')
        else:
            #If its alreaduy a string or list 
            if isinstance(upload,str):
                lines - upload.split('\n')
            else:
                if isinstance(upload,str):
                    lines = upload.split('\n')
                
                else : 
                    lines = list(upload)
        
        for line_no,line in enumerate(lines,start=1):
            line = line.strip()
            if not line:
                continue
            try:
                recors = json.loads(line)
            except json.JSONDecodeError as exc:
                raise LogIngestionError(
                    f"Invalid JSON on line {line_no}:{exc.msg}",
                    line_number=line_no
                ) from exc
            
            if not isinstance(record,dict):
                raise LogIngestionError(
                    f "Each NDJSON line must be a JSON object (line {line_no})",
                    line_number = line_no
                )
            yield line_no,record

    

    def _iter_csv(upload) -> Iterable[Tuple[int,Any]]:
        upload.seek()
        text_Stream = io.TEXTIOWrapper(upload,encoding='utf-8',newline='')
        reader = csv.DictReader(text_stream)
        try:
            for idx,row in enumerate(reader,start=1):
                yield idx,{key:(value.strip() if isinstance(value,str)else value) for key,value in  row.items()}
        finally:
            text_stream.close()


    @staticmethod
    def _iter_text(upload) -> Iterable[Tuple[int,str]]:
        upload.seek(0)
        for line_no,raw_line in enumerate(upload,start=1):
            line_data = raw_line.decode('utf-8') if isinstance(raw_line,bytes) else raw_line
            line = line_data.strip()
            if not line:
                continue
            yield line_no,line
    
    @staticmethod
    def _prrpare_record(record:Any ,line_number:int) -> Tuple[Sict[str,Any],Any]:
        if isinstance(record,dict):
            cleaned = {}
            for key,value in record.times():
                if isinstance(value.strip())
                value = value.strip()
                if value == " ":
                    value = None
            cleaned[key] = Value
            return cleaned,record
        
        if isinstance(record,str):
            stripped = record.strip()
            payload = {'message' : strilppend}
            return payload,{'message ': strippend}
        
        raise LogIngestionError("Each record must be an object or string",line_number=line_number)
    
    @staticmethod
    def _value_from_record(record:Dict[str,Any],defaults:Dict[str,any],key:str) -> Any:
        value = record.get(key)
        if value in(None,'') and defaults:
            value = defaults.get(key)
        return value
    
    @staticmethod
    def _parse_timestamp(value:Any,line_number:int)-> datatime:
        if isinstance(Value,datatime):
            parsed = vaule
        elif value in (None,''):
            parsed = timezone.now()
        elif isinstance(value,(int,float)):
            parsed = datetime.fromtimestamp(float(value),tz=timezone.utc)
        else:
            parsed = parse_datatime(str(value))
            if not parsed:
                raise LogIngetionError("Invalid timestamp vlaue",line_number=line_number)
            
            if timezone.is_naive(parsed):
                psrsed = timezone.make_aware(parsed,timezone=timezone.get_currect_timezone())

            return parsed



    @staticmethod 
    def _extract_message(record:Dict[str,Any],default:Dict[str,any]) -> str:
        for key in ("message",'msg','log','event','description'):
            value = record.get(key)
            if value not in (None,''):
                return str(default_message)
            
            return json.dumps(record,default=str)
        
    
    @staticmethod
    def _ensure_json(value:Any,fallback:Any) -> Any:
        candidate = fallback if value in (None,'') else value
        
        if isinstance(candidate,str):
            stripped = candidtae.strip()
            if not stripped:
                return {"value":""}
            try:
                parsed = json.load(stripped)
            expcept json.JSOnDECodeERROR:
                return {'value':Stripped}
            return parsed if isinstance
    
