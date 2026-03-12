# BI Migration Agent: MicroStrategy to Power BI

An enterprise-grade AI-powered agent workflow for orchestrating complex MicroStrategy to Power BI migrations. This comprehensive system includes knowledge bases, tools, automated validation, security implementation, and complete documentation.

## 🎯 Overview

A production-ready BI migration agent configured with:
- **AI Engine:** AzureOpenAI (GPT-4o)
- **6 Intelligent Tools:** Analysis, code generation, validation, security mapping, reporting, performance optimization
- **30-Day Timeline:** Proven 6-phase migration methodology
- **Enterprise Features:** Risk management, success criteria, comprehensive documentation

## 📚 Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [00_START_HERE.md](00_START_HERE.md) | Executive summary & next steps | 5 min |
| [INDEX.md](INDEX.md) | Master navigation guide | 10 min |
| [bi_migration_agent_config.md](bi_migration_agent_config.md) | **Main configuration** (start with this) | 45 min |
| [knowledge_base.md](knowledge_base.md) | Technical reference library | 60 min |
| [agent_instructions.md](agent_instructions.md) | Behavioral guidelines | 30 min |
| [tool_specifications.md](tool_specifications.md) | Tool technical specs | 40 min |
| [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) | Quick reference & decision matrices | 20 min |
| [agent_config.py](agent_config.py) | Python implementation | 15 min |

## 🚀 Quick Start

1. **Read:** [00_START_HERE.md](00_START_HERE.md) (5 minutes)
2. **Review:** [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) (15 minutes)
3. **Configure:** Set Azure OpenAI credentials
4. **Initialize:** `python agent_config.py`
5. **Begin:** Assessment Phase following phase guidelines

## 🛠 6 AI-Powered Tools

1. **MicroStrategy Object Analyzer** - Parse and assess source complexity
2. **DAX Formula Generator** - Convert metrics to Power BI DAX
3. **Transformation Validator** - Validate migration accuracy
4. **Security Model Mapper** - Design RLS implementation
5. **Migration Report Generator** - Create documentation
6. **Model Performance Analyzer** - Optimize results

## 📅 30-Day Migration Timeline

- **Phase 1 (Days 1-3):** Assessment & Planning
- **Phase 2 (Days 4-7):** Design & Architecture
- **Phase 3 (Days 8-20):** Development
- **Phase 4 (Days 21-25):** Testing & Optimization
- **Phase 5 (Days 26-27):** Cutover & Go-Live
- **Phase 6 (Days 28-30):** Knowledge Transfer & Handoff

## ⚙️ Configuration

### AI Engine Selection
**Chosen:** AzureOpenAI with GPT-4o
- Enterprise security (SOC 2 Type II)
- Native Power BI integration
- Superior BI logic reasoning

### Behavior Preset
```yaml
Temperature:        0.3       # Deterministic output
Top P:             0.9       # Balanced approach
Max Iterations:    10        # Safeguard loops
Max RPM:           60        # Rate limiting
Max Execution:     300 sec   # 5-minute timeout
```

## 📋 Key Features

✅ **Comprehensive Knowledge Base** - 100+ pages of technical reference
✅ **Automated Validation** - Compare MicroStrategy vs Power BI results
✅ **Security Implementation** - RLS patterns with code examples
✅ **Performance Optimization** - Benchmarking and tuning strategies
✅ **Risk Management** - 6 identified risks with mitigation
✅ **Success Criteria** - Clear go/no-go gates for each phase
✅ **Python Integration** - Ready-to-integrate configuration
✅ **Complete Documentation** - All templates and procedures included

## 🔒 Security

- RLS implementation patterns (3 scenarios)
- Security mapping from MicroStrategy
- Dynamic and static RLS approaches
- User-based, role-based, and hierarchical security

## 📊 Quality Metrics

- Data Variance: <0.5% on financial metrics
- Query Performance: <5 seconds P90
- Model Size: <2GB
- User Adoption: >80% within 30 days
- Documentation: 100% complete by handoff

## 🎓 Next Steps

1. Review [00_START_HERE.md](00_START_HERE.md)
2. Assess your MicroStrategy environment
3. Configure Azure OpenAI endpoint
4. Begin Assessment Phase (Phase 1)
5. Track progress using success criteria

## 📞 Support

- Refer to [INDEX.md](INDEX.md) for navigation and cross-references
- Technical questions → [knowledge_base.md](knowledge_base.md)
- Configuration issues → [agent_config.py](agent_config.py)
- Decision support → [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)

## 📄 Files

```
├── 00_START_HERE.md                    # Start here
├── INDEX.md                             # Navigation guide
├── bi_migration_agent_config.md         # Main configuration
├── knowledge_base.md                    # Technical reference
├── agent_instructions.md                # Behavioral guidelines
├── tool_specifications.md               # Tool specifications
├── MIGRATION_GUIDE.md                   # Quick reference
├── agent_config.py                      # Python implementation
├── .gitignore                           # Git ignore rules
└── .env.example                         # Environment template
```

## 🎉 Status

**✅ Complete and Ready for Implementation**

Version: 1.0.0  
Created: March 12, 2026  
Last Updated: March 12, 2026

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```

   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and update with your MicroStrategy credentials:
   ```
   MSTR_USERNAME=your_username
   MSTR_PASSWORD=your_password
   MSTR_API_BASE_URL=https://demo.microstrategy.com/MicroStrategyLibrary/api
   ```

## Running the Application

1. **Start the FastAPI server**
   ```bash
   python main.py
   ```

   Or with uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open your browser**
   Navigate to: `http://localhost:8000`

3. **Use the application**
   - Upload a .MSTR file and/or database query file
   - Click "Process Files" to extract metadata
   - Preview the extracted data
   - Download project and report metadata as JSON files

## API Endpoints

### Upload and Extract Files
- **POST** `/api/upload-files`
  - Upload MSTR and DB query files
  - Returns extracted metadata

### Download Project Metadata
- **POST** `/api/download-project-metadata`
  - Downloads project metadata as JSON file
  - Optional: Include MSTR file for additional context

### Download Report Metadata
- **POST** `/api/download-report-metadata`
  - Downloads report metadata as JSON file
  - Optional: Include MSTR and DB query files

### Health Check
- **GET** `/api/health`
  - Returns application health status

## Supported File Types

- **MSTR Files**: `.mstr`, `.xml`, `.json`
- **Database Query Files**: `.sql`, `.txt`, `.query`

## MicroStrategy REST APIs Used

The application leverages the following MSTR API endpoints:

- `/api/auth/login` - Authentication
- `/api/projects` - List all projects
- `/api/projects/{projectId}` - Get project details
- `/api/projects/{projectId}/reports` - List reports in a project
- `/api/projects/{projectId}/reports/{reportId}` - Get report details

Reference: https://demo.microstrategy.com/MicroStrategyLibrary/api-docs/index.html

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
MSTR_USERNAME=administrator
MSTR_PASSWORD=microstrategy
MSTR_API_BASE_URL=https://demo.microstrategy.com/MicroStrategyLibrary/api
```

### Server Configuration

Edit `main.py` to customize:
- **Port**: Change `port=8000` in the `uvicorn.run()` call
- **Host**: Change `host="0.0.0.0"` for different network access
- **Auto-reload**: Set `reload=False` for production

## Usage Examples

### Example 1: Extract Project Metadata

1. Upload a MSTR configuration file
2. Click "Process Files"
3. In the preview, review the project information
4. Click "Download Project Metadata (JSON)"
5. JSON file will be downloaded with project details

### Example 2: Extract Report Metadata

1. Upload both a MSTR file and database query file
2. Click "Process Files"
3. In the preview, review the available reports
4. Click "Download Report Metadata (JSON)"
5. JSON file will be downloaded with all report metadata

## Error Handling

The application includes comprehensive error handling:

- **File Upload Errors**: Validates file types and sizes
- **MSTR API Errors**: Handles authentication and connection failures
- **Processing Errors**: User-friendly error messages displayed in UI

## Output Format

### Project Metadata JSON
```json
{
  "extraction_timestamp": "2026-03-11T10:30:45.123456",
  "project_metadata": { ... },
  "api_project_info": {
    "id": "...",
    "name": "...",
    "description": "..."
  }
}
```

### Report Metadata JSON
```json
{
  "extraction_timestamp": "2026-03-11T10:30:45.123456",
  "reports": [
    {
      "id": "...",
      "name": "...",
      "type": "...",
      "metadata": { ... }
    }
  ]
}
```

## Troubleshooting

### Port Already in Use
If port 8000 is already in use:
```bash
uvicorn main:app --port 8001
```

### MSTR Authentication Failed
- Verify username and password in `.env`
- Check network connectivity to MicroStrategy server
- Ensure MicroStrategy REST APIs are accessible

### File Upload Issues
- Check file size (recommended: < 50MB)
- Ensure file format is supported
- Check browser console for detailed errors (F12)

### Missing Dependencies
If you see import errors:
```bash
pip install --upgrade -r requirements.txt
```

## Development

### Adding New Features

To add new MSTR API endpoints:

1. Add methods to the `MSTRMetadataExtractor` class
2. Create new FastAPI endpoints in `main.py`
3. Add corresponding buttons/handlers in `static/script.js`
4. Update HTML form in `static/index.html`

### Code Structure

- **main.py**: FastAPI app, API endpoints, metadata extraction logic
- **static/index.html**: Web UI structure
- **static/styles.css**: Responsive styling
- **static/script.js**: Client-side form handling and API calls

## Security Considerations

- **Credentials**: Store MSTR credentials in `.env` (never commit to git)
- **File Upload**: Validate all uploaded files
- **API Tokens**: Session tokens are stored server-side only
- **HTTPS**: Use HTTPS in production

## Performance Tips

- For large files, processing may take time - be patient
- The application limits reports preview to first 10 records
- Adjust limits in `main.py` MSTRMetadataExtractor methods as needed

## Known Limitations

- Supports MicroStrategy REST API endpoints listed above
- Report metadata limited to first 5 reports for performance
- Temporary files are created in system temp directory
- File upload size limited by server configuration

## Future Enhancements

- [ ] Batch processing multiple MSTR files
- [ ] Export to CSV, XML formats
- [ ] Advanced filtering and search
- [ ] Scheduled metadata extraction
- [ ] Database integration for storing metadata history
- [ ] User authentication for the web app
- [ ] Custom report generation
- [ ] Comparison between MSTR versions

## License

This project is provided as-is for MicroStrategy metadata extraction purposes.

## Support

For issues with MicroStrategy REST APIs, refer to:
https://demo.microstrategy.com/MicroStrategyLibrary/api-docs/index.html

For FastAPI documentation:
https://fastapi.tiangolo.com/

## Changelog

### v1.0.0 (2026-03-11)
- Initial release
- File upload functionality
- Project metadata extraction
- Report metadata extraction
- Responsive web UI
