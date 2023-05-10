// ORM class for table 'trips'
// WARNING: This class is AUTO-GENERATED. Modify at your own risk.
//
// Debug information:
// Generated date: Sun May 07 16:30:16 UTC 2023
// For connector: org.apache.sqoop.manager.PostgresqlManager
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapred.lib.db.DBWritable;
import com.cloudera.sqoop.lib.JdbcWritableBridge;
import com.cloudera.sqoop.lib.DelimiterSet;
import com.cloudera.sqoop.lib.FieldFormatter;
import com.cloudera.sqoop.lib.RecordParser;
import com.cloudera.sqoop.lib.BooleanParser;
import com.cloudera.sqoop.lib.BlobRef;
import com.cloudera.sqoop.lib.ClobRef;
import com.cloudera.sqoop.lib.LargeObjectLoader;
import com.cloudera.sqoop.lib.SqoopRecord;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.sql.Date;
import java.sql.Time;
import java.sql.Timestamp;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

public class trips extends SqoopRecord  implements DBWritable, Writable {
  private final int PROTOCOL_VERSION = 3;
  public int getClassFormatVersion() { return PROTOCOL_VERSION; }
  public static interface FieldSetterCommand {    void setField(Object value);  }  protected ResultSet __cur_result_set;
  private Map<String, FieldSetterCommand> setters = new HashMap<String, FieldSetterCommand>();
  private void init0() {
    setters.put("trip_id", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        trip_id = (String)value;
      }
    });
    setters.put("call_type", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        call_type = (String)value;
      }
    });
    setters.put("origin_call", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        origin_call = (Double)value;
      }
    });
    setters.put("origin_stand", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        origin_stand = (Double)value;
      }
    });
    setters.put("taxi_id", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        taxi_id = (Integer)value;
      }
    });
    setters.put("timestamp", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        timestamp = (Long)value;
      }
    });
    setters.put("day_type", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        day_type = (String)value;
      }
    });
    setters.put("missing_data", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        missing_data = (Boolean)value;
      }
    });
    setters.put("polyline", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        polyline = (String)value;
      }
    });
  }
  public trips() {
    init0();
  }
  private String trip_id;
  public String get_trip_id() {
    return trip_id;
  }
  public void set_trip_id(String trip_id) {
    this.trip_id = trip_id;
  }
  public trips with_trip_id(String trip_id) {
    this.trip_id = trip_id;
    return this;
  }
  private String call_type;
  public String get_call_type() {
    return call_type;
  }
  public void set_call_type(String call_type) {
    this.call_type = call_type;
  }
  public trips with_call_type(String call_type) {
    this.call_type = call_type;
    return this;
  }
  private Double origin_call;
  public Double get_origin_call() {
    return origin_call;
  }
  public void set_origin_call(Double origin_call) {
    this.origin_call = origin_call;
  }
  public trips with_origin_call(Double origin_call) {
    this.origin_call = origin_call;
    return this;
  }
  private Double origin_stand;
  public Double get_origin_stand() {
    return origin_stand;
  }
  public void set_origin_stand(Double origin_stand) {
    this.origin_stand = origin_stand;
  }
  public trips with_origin_stand(Double origin_stand) {
    this.origin_stand = origin_stand;
    return this;
  }
  private Integer taxi_id;
  public Integer get_taxi_id() {
    return taxi_id;
  }
  public void set_taxi_id(Integer taxi_id) {
    this.taxi_id = taxi_id;
  }
  public trips with_taxi_id(Integer taxi_id) {
    this.taxi_id = taxi_id;
    return this;
  }
  private Long timestamp;
  public Long get_timestamp() {
    return timestamp;
  }
  public void set_timestamp(Long timestamp) {
    this.timestamp = timestamp;
  }
  public trips with_timestamp(Long timestamp) {
    this.timestamp = timestamp;
    return this;
  }
  private String day_type;
  public String get_day_type() {
    return day_type;
  }
  public void set_day_type(String day_type) {
    this.day_type = day_type;
  }
  public trips with_day_type(String day_type) {
    this.day_type = day_type;
    return this;
  }
  private Boolean missing_data;
  public Boolean get_missing_data() {
    return missing_data;
  }
  public void set_missing_data(Boolean missing_data) {
    this.missing_data = missing_data;
  }
  public trips with_missing_data(Boolean missing_data) {
    this.missing_data = missing_data;
    return this;
  }
  private String polyline;
  public String get_polyline() {
    return polyline;
  }
  public void set_polyline(String polyline) {
    this.polyline = polyline;
  }
  public trips with_polyline(String polyline) {
    this.polyline = polyline;
    return this;
  }
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof trips)) {
      return false;
    }
    trips that = (trips) o;
    boolean equal = true;
    equal = equal && (this.trip_id == null ? that.trip_id == null : this.trip_id.equals(that.trip_id));
    equal = equal && (this.call_type == null ? that.call_type == null : this.call_type.equals(that.call_type));
    equal = equal && (this.origin_call == null ? that.origin_call == null : this.origin_call.equals(that.origin_call));
    equal = equal && (this.origin_stand == null ? that.origin_stand == null : this.origin_stand.equals(that.origin_stand));
    equal = equal && (this.taxi_id == null ? that.taxi_id == null : this.taxi_id.equals(that.taxi_id));
    equal = equal && (this.timestamp == null ? that.timestamp == null : this.timestamp.equals(that.timestamp));
    equal = equal && (this.day_type == null ? that.day_type == null : this.day_type.equals(that.day_type));
    equal = equal && (this.missing_data == null ? that.missing_data == null : this.missing_data.equals(that.missing_data));
    equal = equal && (this.polyline == null ? that.polyline == null : this.polyline.equals(that.polyline));
    return equal;
  }
  public boolean equals0(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof trips)) {
      return false;
    }
    trips that = (trips) o;
    boolean equal = true;
    equal = equal && (this.trip_id == null ? that.trip_id == null : this.trip_id.equals(that.trip_id));
    equal = equal && (this.call_type == null ? that.call_type == null : this.call_type.equals(that.call_type));
    equal = equal && (this.origin_call == null ? that.origin_call == null : this.origin_call.equals(that.origin_call));
    equal = equal && (this.origin_stand == null ? that.origin_stand == null : this.origin_stand.equals(that.origin_stand));
    equal = equal && (this.taxi_id == null ? that.taxi_id == null : this.taxi_id.equals(that.taxi_id));
    equal = equal && (this.timestamp == null ? that.timestamp == null : this.timestamp.equals(that.timestamp));
    equal = equal && (this.day_type == null ? that.day_type == null : this.day_type.equals(that.day_type));
    equal = equal && (this.missing_data == null ? that.missing_data == null : this.missing_data.equals(that.missing_data));
    equal = equal && (this.polyline == null ? that.polyline == null : this.polyline.equals(that.polyline));
    return equal;
  }
  public void readFields(ResultSet __dbResults) throws SQLException {
    this.__cur_result_set = __dbResults;
    this.trip_id = JdbcWritableBridge.readString(1, __dbResults);
    this.call_type = JdbcWritableBridge.readString(2, __dbResults);
    this.origin_call = JdbcWritableBridge.readDouble(3, __dbResults);
    this.origin_stand = JdbcWritableBridge.readDouble(4, __dbResults);
    this.taxi_id = JdbcWritableBridge.readInteger(5, __dbResults);
    this.timestamp = JdbcWritableBridge.readLong(6, __dbResults);
    this.day_type = JdbcWritableBridge.readString(7, __dbResults);
    this.missing_data = JdbcWritableBridge.readBoolean(8, __dbResults);
    this.polyline = JdbcWritableBridge.readString(9, __dbResults);
  }
  public void readFields0(ResultSet __dbResults) throws SQLException {
    this.trip_id = JdbcWritableBridge.readString(1, __dbResults);
    this.call_type = JdbcWritableBridge.readString(2, __dbResults);
    this.origin_call = JdbcWritableBridge.readDouble(3, __dbResults);
    this.origin_stand = JdbcWritableBridge.readDouble(4, __dbResults);
    this.taxi_id = JdbcWritableBridge.readInteger(5, __dbResults);
    this.timestamp = JdbcWritableBridge.readLong(6, __dbResults);
    this.day_type = JdbcWritableBridge.readString(7, __dbResults);
    this.missing_data = JdbcWritableBridge.readBoolean(8, __dbResults);
    this.polyline = JdbcWritableBridge.readString(9, __dbResults);
  }
  public void loadLargeObjects(LargeObjectLoader __loader)
      throws SQLException, IOException, InterruptedException {
  }
  public void loadLargeObjects0(LargeObjectLoader __loader)
      throws SQLException, IOException, InterruptedException {
  }
  public void write(PreparedStatement __dbStmt) throws SQLException {
    write(__dbStmt, 0);
  }

  public int write(PreparedStatement __dbStmt, int __off) throws SQLException {
    JdbcWritableBridge.writeString(trip_id, 1 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(call_type, 2 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeDouble(origin_call, 3 + __off, 8, __dbStmt);
    JdbcWritableBridge.writeDouble(origin_stand, 4 + __off, 8, __dbStmt);
    JdbcWritableBridge.writeInteger(taxi_id, 5 + __off, 4, __dbStmt);
    JdbcWritableBridge.writeLong(timestamp, 6 + __off, -5, __dbStmt);
    JdbcWritableBridge.writeString(day_type, 7 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeBoolean(missing_data, 8 + __off, -7, __dbStmt);
    JdbcWritableBridge.writeString(polyline, 9 + __off, 12, __dbStmt);
    return 9;
  }
  public void write0(PreparedStatement __dbStmt, int __off) throws SQLException {
    JdbcWritableBridge.writeString(trip_id, 1 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(call_type, 2 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeDouble(origin_call, 3 + __off, 8, __dbStmt);
    JdbcWritableBridge.writeDouble(origin_stand, 4 + __off, 8, __dbStmt);
    JdbcWritableBridge.writeInteger(taxi_id, 5 + __off, 4, __dbStmt);
    JdbcWritableBridge.writeLong(timestamp, 6 + __off, -5, __dbStmt);
    JdbcWritableBridge.writeString(day_type, 7 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeBoolean(missing_data, 8 + __off, -7, __dbStmt);
    JdbcWritableBridge.writeString(polyline, 9 + __off, 12, __dbStmt);
  }
  public void readFields(DataInput __dataIn) throws IOException {
this.readFields0(__dataIn);  }
  public void readFields0(DataInput __dataIn) throws IOException {
    if (__dataIn.readBoolean()) { 
        this.trip_id = null;
    } else {
    this.trip_id = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.call_type = null;
    } else {
    this.call_type = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.origin_call = null;
    } else {
    this.origin_call = Double.valueOf(__dataIn.readDouble());
    }
    if (__dataIn.readBoolean()) { 
        this.origin_stand = null;
    } else {
    this.origin_stand = Double.valueOf(__dataIn.readDouble());
    }
    if (__dataIn.readBoolean()) { 
        this.taxi_id = null;
    } else {
    this.taxi_id = Integer.valueOf(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.timestamp = null;
    } else {
    this.timestamp = Long.valueOf(__dataIn.readLong());
    }
    if (__dataIn.readBoolean()) { 
        this.day_type = null;
    } else {
    this.day_type = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.missing_data = null;
    } else {
    this.missing_data = Boolean.valueOf(__dataIn.readBoolean());
    }
    if (__dataIn.readBoolean()) { 
        this.polyline = null;
    } else {
    this.polyline = Text.readString(__dataIn);
    }
  }
  public void write(DataOutput __dataOut) throws IOException {
    if (null == this.trip_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, trip_id);
    }
    if (null == this.call_type) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, call_type);
    }
    if (null == this.origin_call) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeDouble(this.origin_call);
    }
    if (null == this.origin_stand) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeDouble(this.origin_stand);
    }
    if (null == this.taxi_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeInt(this.taxi_id);
    }
    if (null == this.timestamp) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.timestamp);
    }
    if (null == this.day_type) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, day_type);
    }
    if (null == this.missing_data) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeBoolean(this.missing_data);
    }
    if (null == this.polyline) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, polyline);
    }
  }
  public void write0(DataOutput __dataOut) throws IOException {
    if (null == this.trip_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, trip_id);
    }
    if (null == this.call_type) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, call_type);
    }
    if (null == this.origin_call) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeDouble(this.origin_call);
    }
    if (null == this.origin_stand) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeDouble(this.origin_stand);
    }
    if (null == this.taxi_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeInt(this.taxi_id);
    }
    if (null == this.timestamp) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.timestamp);
    }
    if (null == this.day_type) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, day_type);
    }
    if (null == this.missing_data) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeBoolean(this.missing_data);
    }
    if (null == this.polyline) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, polyline);
    }
  }
  private static final DelimiterSet __outputDelimiters = new DelimiterSet((char) 44, (char) 10, (char) 0, (char) 0, false);
  public String toString() {
    return toString(__outputDelimiters, true);
  }
  public String toString(DelimiterSet delimiters) {
    return toString(delimiters, true);
  }
  public String toString(boolean useRecordDelim) {
    return toString(__outputDelimiters, useRecordDelim);
  }
  public String toString(DelimiterSet delimiters, boolean useRecordDelim) {
    StringBuilder __sb = new StringBuilder();
    char fieldDelim = delimiters.getFieldsTerminatedBy();
    __sb.append(FieldFormatter.escapeAndEnclose(trip_id==null?"null":trip_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(call_type==null?"null":call_type, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(origin_call==null?"null":"" + origin_call, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(origin_stand==null?"null":"" + origin_stand, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(taxi_id==null?"null":"" + taxi_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(timestamp==null?"null":"" + timestamp, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(day_type==null?"null":day_type, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(missing_data==null?"null":"" + missing_data, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(polyline==null?"null":polyline, delimiters));
    if (useRecordDelim) {
      __sb.append(delimiters.getLinesTerminatedBy());
    }
    return __sb.toString();
  }
  public void toString0(DelimiterSet delimiters, StringBuilder __sb, char fieldDelim) {
    __sb.append(FieldFormatter.escapeAndEnclose(trip_id==null?"null":trip_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(call_type==null?"null":call_type, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(origin_call==null?"null":"" + origin_call, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(origin_stand==null?"null":"" + origin_stand, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(taxi_id==null?"null":"" + taxi_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(timestamp==null?"null":"" + timestamp, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(day_type==null?"null":day_type, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(missing_data==null?"null":"" + missing_data, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(polyline==null?"null":polyline, delimiters));
  }
  private static final DelimiterSet __inputDelimiters = new DelimiterSet((char) 44, (char) 10, (char) 0, (char) 0, false);
  private RecordParser __parser;
  public void parse(Text __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(CharSequence __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(byte [] __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(char [] __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(ByteBuffer __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(CharBuffer __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  private void __loadFromFields(List<String> fields) {
    Iterator<String> __it = fields.listIterator();
    String __cur_str = null;
    try {
    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.trip_id = null; } else {
      this.trip_id = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.call_type = null; } else {
      this.call_type = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.origin_call = null; } else {
      this.origin_call = Double.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.origin_stand = null; } else {
      this.origin_stand = Double.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.taxi_id = null; } else {
      this.taxi_id = Integer.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.timestamp = null; } else {
      this.timestamp = Long.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.day_type = null; } else {
      this.day_type = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.missing_data = null; } else {
      this.missing_data = BooleanParser.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.polyline = null; } else {
      this.polyline = __cur_str;
    }

    } catch (RuntimeException e) {    throw new RuntimeException("Can't parse input data: '" + __cur_str + "'", e);    }  }

  private void __loadFromFields0(Iterator<String> __it) {
    String __cur_str = null;
    try {
    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.trip_id = null; } else {
      this.trip_id = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.call_type = null; } else {
      this.call_type = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.origin_call = null; } else {
      this.origin_call = Double.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.origin_stand = null; } else {
      this.origin_stand = Double.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.taxi_id = null; } else {
      this.taxi_id = Integer.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.timestamp = null; } else {
      this.timestamp = Long.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.day_type = null; } else {
      this.day_type = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.missing_data = null; } else {
      this.missing_data = BooleanParser.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.polyline = null; } else {
      this.polyline = __cur_str;
    }

    } catch (RuntimeException e) {    throw new RuntimeException("Can't parse input data: '" + __cur_str + "'", e);    }  }

  public Object clone() throws CloneNotSupportedException {
    trips o = (trips) super.clone();
    return o;
  }

  public void clone0(trips o) throws CloneNotSupportedException {
  }

  public Map<String, Object> getFieldMap() {
    Map<String, Object> __sqoop$field_map = new HashMap<String, Object>();
    __sqoop$field_map.put("trip_id", this.trip_id);
    __sqoop$field_map.put("call_type", this.call_type);
    __sqoop$field_map.put("origin_call", this.origin_call);
    __sqoop$field_map.put("origin_stand", this.origin_stand);
    __sqoop$field_map.put("taxi_id", this.taxi_id);
    __sqoop$field_map.put("timestamp", this.timestamp);
    __sqoop$field_map.put("day_type", this.day_type);
    __sqoop$field_map.put("missing_data", this.missing_data);
    __sqoop$field_map.put("polyline", this.polyline);
    return __sqoop$field_map;
  }

  public void getFieldMap0(Map<String, Object> __sqoop$field_map) {
    __sqoop$field_map.put("trip_id", this.trip_id);
    __sqoop$field_map.put("call_type", this.call_type);
    __sqoop$field_map.put("origin_call", this.origin_call);
    __sqoop$field_map.put("origin_stand", this.origin_stand);
    __sqoop$field_map.put("taxi_id", this.taxi_id);
    __sqoop$field_map.put("timestamp", this.timestamp);
    __sqoop$field_map.put("day_type", this.day_type);
    __sqoop$field_map.put("missing_data", this.missing_data);
    __sqoop$field_map.put("polyline", this.polyline);
  }

  public void setField(String __fieldName, Object __fieldVal) {
    if (!setters.containsKey(__fieldName)) {
      throw new RuntimeException("No such field:"+__fieldName);
    }
    setters.get(__fieldName).setField(__fieldVal);
  }

}
