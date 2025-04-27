# AVL Inventory Manager: Master Project Plan

## ✅ Current Completed Features
- Flask app with SQLAlchemy database
- User Management: Add, Edit, Delete Users
- Inventory Management: Add, Edit, Soft Delete Items
- Bootstrap UI with Modals for Adding/Editing
- Datatables integration (search, sort, paginate)
- Last Updated and Date Added tracking for Inventory
- Safe soft-delete (is_active=False) for inventory items
- Flash messages for success/error notifications
- Field normalization (None vs empty strings)
- Mobile and Desktop Responsive Layout
- Local Bootstrap Icons
- Placeholders and Labels for form fields
- Datatables functional polish

---

## 🔧 Features Currently In Progress
- Building proper Edit Modals (labels + placeholders)
- Making fields user-friendly even when pre-filled
- Final visual polish

---

## 🚀 Next Planned Features
1. **User-friendly History Tracking**
   - Log item additions, edits, deletions
   - Allow browsing past actions

2. **Retrieval System**
   - 'Take' items from inventory
   - Capture retriever's name, quantity, purpose

3. **Low Stock Alerts**
   - Highlight items below min_stock threshold

4. **Reports Generation**
   - Export inventory/history to CSV or Excel

5. **Data Backup and Restore**
   - Implement database backup strategy

6. **(Optional) UI Polishing**
   - Add subtle animations (modals, flash messages)
   - Add inventory filters (by category/location)

---

## ✨ Bonus Feature Ideas
- Print-friendly view for inventory
- Pagination and search control improvements
- Email notifications for low stock
- Password protection (if needed)
- Multi-user support (if project expands)

---

## 🗂 Organizational Structure
| File | Purpose |
|-----|---------|
| `app.py` | Main Flask Application |
| `templates/` | HTML Templates (index, users, etc.) |
| `static/` | Bootstrap, Datatables, Backgrounds, Icons |
| `users.sqlite3` | Database file |

---

## 📂 Milestone Tracker
| Status | Feature |
|:------:|:-------|
| ✅ | Add/Edit/Delete Users |
| ✅ | Add/Edit/Delete Inventory Items |
| ✅ | Datatables and Bootstrap Modals |
| ✅ | Field Normalization Improvements |
| 🔄 | History Tracking |
| 🔄 | Retrieval System |
| 🔄 | Low Stock Warnings |
| 🔄 | Reporting and Backup |

---