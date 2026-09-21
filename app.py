from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from models import db, Candidate, Job
import os
import json

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["Content-Type"])

# Use PostgreSQL in production if DATABASE_URL is set, otherwise use SQLite
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Neon PostgreSQL uses postgresql:// protocol
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def seed_data():
    if Candidate.query.first() is None:
        abrar = Candidate(
            name="Abrar",
            skills="CAD & Design Software: AutoCAD, Revit, SolidWorks, 2D Drafting, 3D Modeling, CAD Design, Engineering Drawings, Technical Drawings, Floor Plans, Elevations, Site Layouts, Assembly Drawings, Fabrication Drawings. Mechanical & Construction Drafting: Geometric Dimensioning & Tolerancing (GD&T), ASME Standards, ANSI Standards, Dimensional Tolerancing, Manufacturing Drawings, Construction Drawings, Engineering Schematics, Material Specifications, Field Measurements, Blueprint Interpretation. Drawing Control & Documentation: Redline Markups, Engineering Change Revisions, Revision Control, Document Control, Drawing Database Management, Legacy Drawing Conversion, Bill of Materials (BOM), Assembly Instructions, Technical Documentation, Drawing Archiving, Microsoft Excel. Quality & Project Support: QA/QC, Drawing Verification, Dimensional Accuracy, Constructability Review, Design Conflict Resolution, Design Review, Field Note Verification, Procurement Support, Manufacturing Support, Cross-Functional Collaboration (CAD). GIS Software & Platforms: ArcGIS Pro, ArcGIS Online, QGIS, Cityworks, Mobile GIS Applications. Spatial Data Management: Geodatabases, Spatial Databases, Data Editing, Feature Digitization, Attribute Management, Data Validation, Data Maintenance, Asset Data Management. Mapping & Spatial Analysis: Cartographic Design, Map Production, Thematic Mapping, Spatial Queries, Geoprocessing, Spatial Analysis, Data Visualization, Infrastructure & Land-Use Mapping. GIS Data & Formats: Shapefile, GeoJSON, KML, Vector Data, Spatial Data Conversion, Data Preparation, Database Structures. QA/QC & Field Data: GIS QA/QC, Spatial Data Validation, Attribute Verification, Field Data Collection, GPS-Based Data Capture, Infrastructure Documentation, Data Discrepancy Resolution. Documentation & Collaboration: Metadata Management, SOP Documentation, Work Orders, Asset Tracking, Technical Reporting, Engineering Coordination, Stakeholder Support (GIS). OSP & Fiber Design: FTTx, FTTH, XGS-PON, OSP Network Design, Aerial & Underground Fiber Design, HLD, LLD, Distribution & Backbone Networks, F1–F4 Fiber Distribution, 1:32 PON Architecture, Splice Matrices, Splitter Layouts. CAD, GIS & Mapping: AutoCAD, ArcGIS, ArcGIS Field Maps, GIS Mapping, Geo-Referenced Basemaps, GPS Data Collection, Construction Drawings, As-Built Drawings, Engineering Redlines, CAD Layer Management, Spatial Data Editing. OSP Infrastructure, Permitting & QA/QC: Conduit Routing, Bore Paths, Handhole Placement, Pole Attachments, ROW Alignment, Right-of-Way Offsets, Aerial Clearances, Underground Pathways, Constructability Review, ROW Permitting, Permit Packages, Alignment Plans, NESC, DOT Requirements, Utility Standards, Jurisdictional Compliance, BOM, BOQ, Conduit Takeoffs, Design QA/QC, Spatial Accuracy, Geometry Validation, Drawing Review, Redline Incorporation, As-Built Documentation. GIS Data & Field Support: Parcel Data, Zoning, Land Use, Infrastructure Mapping, Attribute Data, Mobile Field Forms, GPS Field Verification, Data Digitization, Map Production, Geometry QA/QC (OSP)",
            search_queries='["CAD Drafter", "AutoCAD Drafter", "GIS Specialist", "OSP Engineer", "Fiber Designer"]'
        )
        adnan = Candidate(
            name="Adnan",
            skills="GIS Software & Tools: ArcGIS Pro, AutoCAD Map 3D... Outside Plant Engineering: FTTx... Endpoint Management...",
            search_queries='["GIS Analyst", "OSP Fiber Engineer", "IT Support Engineer"]'
        )
        akib = Candidate(
            name="Akib Zaman",
            skills="CAD Drafting: AutoCAD 2D... OSP, Fiber & GIS Design: FTTH/FTTx...",
            search_queries='["CAD Drafter", "OSP Engineer"]'
        )
        ahmed = Candidate(
            name="Ahmed",
            skills="GIS Software & Platforms: ArcGIS Pro, ArcGIS Online, QGIS, Cityworks, Mobile GIS Applications. Spatial Data Management: Geodatabases, Spatial Databases, Data Editing, Feature Digitization, Attribute Management, Data Validation, Data Maintenance, Asset Data Management. Mapping & Spatial Analysis: Cartographic Design, Map Production, Thematic Mapping, Spatial Queries, Geoprocessing, Spatial Analysis, Data Visualization, Infrastructure & Land-Use Mapping. GIS Data & Formats: Shapefile, GeoJSON, KML, Vector Data, Spatial Data Conversion, Data Preparation, Database Structures. QA/QC & Field Data: GIS QA/QC, Spatial Data Validation, Attribute Verification, Field Data Collection, GPS-Based Data Capture, Infrastructure Documentation, Data Discrepancy Resolution. Documentation & Collaboration: Metadata Management, SOP Documentation, Work Orders, Asset Tracking, Technical Reporting, Engineering Coordination, Stakeholder Support (GIS). OSP Fiber Design & Engineering: FTTx, XGS-PON, Fiber Optic Network Design, Aerial & Underground Design, Pole Line Design, Conduit Pathways, Duct Bank Layouts, Handhole Placement, Fiber Distribution Layouts, Route Design, Constructability Reviews, Field Surveys. GIS & Mapping Tools: 3GIS, GIS Mapping, Google Earth, Geo-Referenced Data, Spatial Data Review, Infrastructure Mapping, Route Analysis, Field Data Integration. Documentation, QA/QC & Project Coordination: HLD/LLD Documentation, Splice Matrices, As-Built Drawings, Redline Updates, Engineering Packages, Submittal Packages, BOM/BOQ Development, Material Estimation, Fiber Loss Calculations, QA/QC, Design Validation, NESC, DOT/Utility Standards, ANSI/ISO Drafting Standards, Permit Coordination, Engineering Coordination, Construction Support, Microsoft Office, Microsoft Visio (OSP). CAD & BIM Software: AutoCAD, Revit, 2D Drafting, 3D Modeling, BIM Workflows. Technical Drafting & Documentation: Construction Drawings, Floor Plans, Elevations, Cross-Sections, Detail Drawings, Shop Drawings, Permit Drawings, As-Built Drawings, Construction Documents, Permit Documentation, Redline Markups, Material Takeoffs, Submittal Packages, Project Closeout Documentation. CAD Management & QA/QC: Layers, Xrefs, Blocks, Title Blocks, Sheet Sets, Dimensioning, Annotation, Scaling, Plotting, Revision Tracking, Drawing QA/QC, Dimensional Accuracy, CAD Standards, Document Control, ANSI/ISO Drafting Standards, Building Code Compliance. Coordination & Project Support: Engineering Coordination, Architectural Coordination, Design Reviews, Client Revisions, Contractor Coordination, Multidisciplinary Collaboration (CAD)",
            search_queries='["GIS Specialist", "Fiber Designer", "OSP Engineer", "AutoCAD Drafter"]'
        )
        geetha = Candidate(
            name="Geetha Ragiphani",
            skills="Infrastructure Operations & Facilities: Data center operations... Server Hardware, Linux & OOB...",
            search_queries='["Data Center Technician", "Data Center Analyst"]'
        )
        rija = Candidate(
            name="Rija Tovi",
            skills="OSP / FTTx Delivery: Distribution-split FTTx... Fiber Design / Documentation: AutoCAD, GIS, ArcGIS...",
            search_queries='["OSP Engineer", "Fiber Broadband Engineer"]'
        )
        mahbubul = Candidate(
            name="Mahbubul Alam",
            skills="Data Center Infrastructure: Tier III Colocation... Server Hardware... Routing & MPLS... ISP...",
            search_queries='["Data Center Technician", "NOC Engineer", "ISP Network Engineer"]'
        )
        najiur = Candidate(
            name="Najiur",
            skills="AutoCAD Drafting: Permit Drawing Packages, Construction Details, Erosion-Control Plans, Drainage Plans, Utility Layouts, Grading Plans, Civil Site Plans, 2D Technical Drawings\nCAD Standards & Document Control: As-Built Documentation, CAD Templates, Revision Control, Drawing Registers, Sheet Organization, Title Blocks, Linetypes, Layers\nTechnical Coordination: Engineering Sketches, Survey Data, Field Measurements, Redline Markups, Municipal Review Comments, Utility Coordination, Constructability Review, Drawing Quality Control\nProject Support: Quantity Takeoffs, Piping and Drainage Materials, Permit Submissions, Technical Documentation, Drawing Reviews, Back-Checks, Deadline Management, Cross-Functional Coordinations",
            search_queries='["CAD Drafter", "AutoCAD Drafter"]'
        )
        nujhat = Candidate(
            name="Nujhat Khan",
            skills="Design & Software: AutoCAD, GIS... Fiber Network Design... BIM & Architectural Production...",
            search_queries='["OSP Engineer", "Architectural Designer"]'
        )
        rayda = Candidate(
            name="Rayda Nur",
            skills="Financial Analysis & Planning... Accounting & Financial Reporting... Operational Accounting...",
            search_queries='["Financial Analyst", "Staff Accountant"]'
        )
        
        db.session.add_all([abrar, adnan, akib, ahmed, geetha, rija, mahbubul, najiur, nujhat, rayda])
        db.session.commit()
        print("Database seeded with all candidates.")

with app.app_context():
    db.create_all()
    seed_data()

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    candidates = Candidate.query.all()
    return jsonify([c.to_dict() for c in candidates])

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    status = request.args.get('status')
    sort_by = request.args.get('sort', 'score_desc')
    state_filter = request.args.get('state')
    date_filter = request.args.get('date') # '1', '3', '7' days ago
    candidate_id = request.args.get('candidate_id')
    
    query = Job.query
    if candidate_id:
        query = query.filter_by(candidate_id=candidate_id)
    if status:
        query = query.filter_by(status=status)
    query = query.filter(Job.source.in_(['LinkedIn', 'Dice']))
        
    jobs = query.all()
    
    filtered_jobs = []
    for job in jobs:
        # Date filter mock logic
        if date_filter:
            try:
                days = int(date_filter)
                if 'hour' not in job.posted_date and 'minute' not in job.posted_date:
                    job_days_str = ''.join(filter(str.isdigit, job.posted_date))
                    if job_days_str and int(job_days_str) > days:
                        continue
            except ValueError:
                pass
        # State filter
        if state_filter and state_filter.lower() not in (job.location or '').lower():
            continue
            
        filtered_jobs.append(job.to_dict())

    # Apply Sorting
    if sort_by == 'score_desc':
        filtered_jobs.sort(key=lambda x: x['match_score'], reverse=True)
    elif sort_by == 'score_asc':
        filtered_jobs.sort(key=lambda x: x['match_score'])
    elif sort_by == 'date_desc':
        filtered_jobs.sort(key=lambda x: x['created_at'], reverse=True)
    elif sort_by == 'date_asc':
        filtered_jobs.sort(key=lambda x: x['created_at'])

    return jsonify(filtered_jobs)

@app.route('/api/jobs/<int:job_id>/status', methods=['PUT'])
def update_job_status(job_id):
    data = request.json
    job = Job.query.get_or_404(job_id)
    if 'status' in data and data['status'] in ['New', 'Applied', 'Dismissed']:
        job.status = data['status']
        db.session.commit()
        return jsonify(job.to_dict())
    return jsonify({'error': 'Invalid status'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
